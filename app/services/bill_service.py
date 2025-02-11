import base64
import logging
import aiohttp
from bs4 import BeautifulSoup
from app.services.slack_service import SlackService
import asyncio
from typing import List, Optional
from app.schemas.bill_schemas import BillResponse
from app.utils.http_utils import DEFAULT_HEADERS, get_bill_headers
import os
from app.models import LegiscanBill, LegiscanSession
from sqlalchemy import and_
from datetime import date
from app.services.session_service import SessionService
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class BillService:
    @staticmethod
    async def get_bill_html(session: aiohttp.ClientSession, bill_number: str) -> Optional[str]:
        url = f"https://www.legis.iowa.gov/docs/publications/LGI/91/attachments/{bill_number}.html?layout=false"
        headers = get_bill_headers(bill_number)
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 404:
                    logger.warning(f"Bill {bill_number} not found (404)")
                    return None
                response.raise_for_status()
                text = await response.text()
                if len(text) < 100:
                    logger.warning(f"Bill {bill_number} returned empty or invalid content")
                    return None
                logger.info(f"Successfully retrieved HTML for bill {bill_number}")
                return text
        except Exception as e:
            logger.error(f"Error fetching bill {bill_number}: {e}")
            return None

    @staticmethod
    def convert_to_base64(html_content: str) -> str:
        return base64.b64encode(html_content.encode()).decode('utf-8')

    @staticmethod
    async def process_bill_results(
        bills_data: list,
        bill_numbers: list,
        results: list,
        state_links: list,
        bill_titles: list
    ) -> List[BillResponse]:
        for bill_number, html_content, state_link, bill_title in zip(bill_numbers, results, state_links, bill_titles):
            if html_content:
                bills_data.append(BillResponse(
                    bill_number=bill_number,
                    bill_title=bill_title,
                    base64_html=BillService.convert_to_base64(html_content),
                    state_link=state_link
                ))
        return bills_data

    @staticmethod
    async def scrape_bills() -> List[BillResponse]:
        logger.info("Starting bill scraping process")
        url = "https://www.legis.iowa.gov/legislation/billTracking/billpacket"
        bills_data = []

        try:
            timeout = aiohttp.ClientTimeout(total=300)
            connector = aiohttp.TCPConnector(limit=10)
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                async with session.get(url, headers=DEFAULT_HEADERS) as response:
                    response.raise_for_status()
                    content = await response.text()
                    
                    soup = BeautifulSoup(content, 'html.parser')
                    # Get all relevant tables (both "Bills Filed" and "Study Bills Filed")
                    tables = soup.find_all('table', class_='standard sortable divideVert')
                    
                    if not tables:
                        logger.error("Could not find any bill tables in page")
                        return []
                    
                    bill_numbers = []
                    state_links = []
                    bill_titles = []
                    tasks = []
                    
                    # Iterate over all found tables
                    for table in tables:
                        # Loop over the table rows (skip rows containing header cells)
                        for row in table.find_all('tr'):
                            if row.find('th'):
                                continue
                            cells = row.find_all('td')
                            if len(cells) < 2:
                                continue
                            # Extract bill number from the first column (from the <a> tag)
                            a_tag = cells[0].find('a')
                            if not a_tag:
                                continue
                            bill_number = a_tag.text.strip().replace(" ", "")
                            state_link = f"https://www.legis.iowa.gov/legislation/BillBook?ba={bill_number}&ga=91"
                            # Extract the bill title from the second column
                            bill_title = cells[1].get_text(separator=" ", strip=True)
                            
                            bill_numbers.append(bill_number)
                            state_links.append(state_link)
                            bill_titles.append(bill_title)
                            tasks.append(BillService.get_bill_html(session, bill_number))
                    
                    results = await asyncio.gather(*tasks)
                    bills_data = await BillService.process_bill_results([], bill_numbers, results, state_links, bill_titles)
            
            logger.info(f"Scraping complete. Successfully processed {len(bills_data)} bills")
            return bills_data
                    
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    @staticmethod
    async def convert_bill_to_markdown(bill_number: str, base64_html: str) -> Optional[dict]:
        formatter_api_url = os.getenv('BILL_FORMATTER_API_BASE_URL')
        if not formatter_api_url:
            logger.error("BILL_FORMATTER_API_BASE_URL environment variable not set")
            return None

        convert_endpoint = f"{formatter_api_url}/api/v1/bill-text/convert"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    convert_endpoint,
                    json={"html_content_base64": base64_html},
                    headers={"Content-Type": "application/json"}
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    
                    return {
                        "bill_number": bill_number,
                        "markdown_text": result["text"]
                    }
                    
        except aiohttp.ClientError as e:
            logger.error(f"Error converting bill {bill_number} to markdown: {str(e)}")
            return None
        except KeyError as e:
            logger.error(f"Unexpected response format for bill {bill_number}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error converting bill {bill_number} to markdown: {str(e)}")
            return None

    @staticmethod
    async def check_for_bills(bill_numbers: List[str], session_id: int, state_code: str) -> List[str]:
        """
        Uses the Upvote API endpoint to check which bills don't exist in Upvote (i.e. are new).
        It returns a list of bill numbers that are missing.
        """
        # Force reload environment variables
        load_dotenv(override=True)
        
        upvote_api_url = os.getenv('UPVOTE_API_BASE_URL')
        upvote_api_key = os.getenv('UPVOTE_API_KEY')
        upvote_uid = os.getenv("UPVOTE_UID")
        access_token = os.getenv("ACCESS_TOKEN")
        client = os.getenv("CLIENT")
        
        # Add detailed environment variable logging
        logger.info("Checking environment variables:")
        logger.info(f"UPVOTE_API_BASE_URL: {'SET' if upvote_api_url else 'MISSING'}")
        logger.info(f"UPVOTE_API_KEY: {'SET' if upvote_api_key else 'MISSING'}")
        logger.info(f"UPVOTE_UID: {'SET' if upvote_uid else 'MISSING'}")
        logger.info(f"ACCESS_TOKEN: {'SET' if access_token else 'MISSING'}")
        logger.info(f"CLIENT: {'SET' if client else 'MISSING'}")
        
        if not upvote_api_url or not upvote_api_key or not upvote_uid or not access_token or not client:
            logger.error("Upvote API configuration is missing in environment variables")
            # If configuration is missing, assume all bills are new
            return bill_numbers

        tasks = []
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            for bill_number in bill_numbers:
                tasks.append(BillService.async_check_bill_exists(
                    session,
                    state_code,
                    session_id,
                    bill_number,
                    upvote_api_url,
                    upvote_api_key,
                    upvote_uid,
                    access_token,
                    client
                ))
            results = await asyncio.gather(*tasks)
        
        missing_bills = []
        for bill_number, result in zip(bill_numbers, results):
            exists = False
            if result and isinstance(result, dict):
                # Add detailed logging for debugging
                logger.info(f"API response for bill {bill_number}: {result}")
                exists = result.get("count", 0) > 0 and "data" in result
            if not exists:
                missing_bills.append(bill_number)
        
        logger.info(f"Found {len(missing_bills)} new bills out of {len(bill_numbers)} checked via Upvote API")
        return missing_bills

    @staticmethod
    async def async_check_bill_exists(http_session: aiohttp.ClientSession, state_code: str, session_id: int, bill_number: str,
                                      upvote_api_url: str, upvote_api_key: str, upvote_uid: str, access_token: str, client: str):
        endpoint = f"{upvote_api_url}/legible/bills/filter"
        params = {
            "state_code": state_code,
            "session_id": session_id,
            "query": bill_number
        }
        headers = {
            "Authorization": f"Bearer {upvote_api_key}",
            "uid": upvote_uid,
            "access_token": access_token,
            "client": client
        }
        try:
            logger.info(f"Checking bill {bill_number}")
            logger.info(f"Endpoint: {endpoint}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Params: {params}")
            
            async with http_session.get(endpoint, params=params, headers=headers) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Response status: {response.status}")
                logger.info(f"Response for bill {bill_number}: {result}")
                return result
        except Exception as e:
            logger.error(f"Error checking bill {bill_number} existence via API: {str(e)}")
            logger.error(f"Full error details: {type(e).__name__}: {str(e)}")
            return None

    @staticmethod
    async def process_new_bills():
        """
        Automated process to scrape, check, and submit new bills.
        A bill is considered new if it is actually sent (POSTed) to the manual_entry endpoint.
        """
        logger.info("=== Starting bill processing job ===")
        try:
            logger.info("Step 1/6: Using hardcoded session ID for Iowa")
            session_id = 937
            logger.info(f"Using session ID: {session_id}")
            
            logger.info("Step 2/6: Checking API configuration")
            upvote_api_url = os.getenv('UPVOTE_API_BASE_URL')
            upvote_api_key = os.getenv('UPVOTE_API_KEY')
            upvote_uid = os.getenv("UPVOTE_UID")
            access_token = os.getenv("ACCESS_TOKEN")
            client = os.getenv("CLIENT")
            
            if not all([upvote_api_url, upvote_api_key, upvote_uid, access_token, client]):
                logger.error("Missing required environment variables")
                logger.info(f"UPVOTE_API_BASE_URL: {'SET' if upvote_api_url else 'MISSING'}")
                logger.info(f"UPVOTE_API_KEY: {'SET' if upvote_api_key else 'MISSING'}")
                logger.info(f"UPVOTE_UID: {'SET' if upvote_uid else 'MISSING'}")
                logger.info(f"ACCESS_TOKEN: {'SET' if access_token else 'MISSING'}")
                logger.info(f"CLIENT: {'SET' if client else 'MISSING'}")
                return
            logger.info("API configuration validated")
            
            logger.info("Step 3/6: Scraping bills from Iowa legislature website")
            bills = await BillService.scrape_bills()
            logger.info(f"Found {len(bills)} total bills")
            
            logger.info("Step 4/6: Checking for new bills")
            bill_numbers = [bill.bill_number for bill in bills]
            new_bills = await BillService.check_for_bills(bill_numbers, session_id, "IA")
            
            total_bills = len(bills)
            if not new_bills:
                logger.info("No new bills found")
                await SlackService.notify_bill_processing(
                    total_bills=total_bills,
                    new_bills=[],
                    duplicate_count=total_bills
                )
                return
            
            logger.info(f"Step 5/6: Submitting {len(new_bills)} new bills to Upvote API")
            endpoint = f"{upvote_api_url}/internal/bills?api_key={upvote_api_key}"
            success_count = 0
            error_count = 0
            submitted_new_bills = []
            
            async with aiohttp.ClientSession() as session:
                for bill_number in new_bills:
                    logger.info(f"Processing bill {bill_number}")
                    bill_data = next((b for b in bills if b.bill_number == bill_number), None)
                    if bill_data:
                        manual_entry = {
                            "bill": {
                                "state_code": "IA",
                                "title": bill_data.bill_title,
                                "summary": bill_data.bill_title,
                                "bill_number": bill_number,
                                "current_state": "introduced",
                                "introduced_date": date.today().strftime("%Y-%m-%d"),
                                "state_link": bill_data.state_link,
                                "bill_text_data_base64": bill_data.base64_html
                            }
                        }
                        
                        try:
                            async with session.post(
                                endpoint,
                                json=manual_entry,
                                headers={"Content-Type": "application/json"}
                            ) as response:
                                response.raise_for_status()
                                success_count += 1
                                submitted_new_bills.append(bill_number)
                                logger.info(f"Successfully submitted bill {bill_number}")
                        except Exception as e:
                            error_count += 1
                            logger.error(f"Error submitting bill {bill_number}: {str(e)}")
            
            await SlackService.notify_bill_processing(
                total_bills=total_bills,
                new_bills=submitted_new_bills,
                duplicate_count=total_bills - len(submitted_new_bills)
            )
            
            logger.info("=== Bill processing complete ===")
            logger.info(f"Summary: {success_count} bills submitted successfully, {error_count} failures")
        except Exception as e:
            logger.error(f"Error in automated bill processing: {str(e)}")
            raise