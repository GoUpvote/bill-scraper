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
from app.database.session import get_db
from app.models import LegiscanBill, LegiscanSession
from sqlalchemy import and_
from datetime import date
from app.services.session_service import SessionService

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
    async def process_bill_results(bills_data: list, bill_numbers: list, results: list, state_links: list) -> List[BillResponse]:
        for bill_number, html_content, state_link in zip(bill_numbers, results, state_links):
            if html_content:
                bills_data.append(BillResponse(
                    bill_number=bill_number,
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
                    bill_table = soup.find('table', class_='standard sortable divideVert')
                    
                    if not bill_table:
                        logger.error("Could not find bill table in page")
                        return []
                    
                    bill_links = bill_table.find_all('a')
                    logger.info(f"Found {len(bill_links)} bills in the table")
                    
                    tasks = []
                    bill_numbers = []
                    state_links = []
                    for link in bill_links:
                        bill_number = link.text.strip().replace(" ", "")
                        state_link = f"https://www.legis.iowa.gov/legislation/BillBook?ba={bill_number}&ga=91"
                        bill_numbers.append(bill_number)
                        state_links.append(state_link)
                        tasks.append(BillService.get_bill_html(session, bill_number))
                    
                    results = await asyncio.gather(*tasks)
                    bills_data = await BillService.process_bill_results([], bill_numbers, results, state_links)
            
            logger.info(f"Scraping complete. Successfully processed {len(bills_data)} bills")
            return bills_data
                    
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    @staticmethod
    async def convert_bill_to_markdown(bill_number: str, base64_html: str) -> Optional[dict]:
        """
        Converts a bill's HTML content to markdown format using the bill formatter API
        
        Args:
            bill_number: The identifier of the bill
            base64_html: Base64 encoded HTML content of the bill
            
        Returns:
            Optional[dict]: Dictionary containing bill_number and markdown text, or None if conversion fails
        """
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
        Checks which bills don't exist in the database for a given session and state
        
        Args:
            bill_numbers: List of bill numbers to check
            session_id: The legislative session ID
            state_code: The state code (e.g., 'IA')
            
        Returns:
            List[str]: List of bill numbers that don't exist in the database
        """
        try:
            with get_db() as db:
                existing_bills = db.query(LegiscanBill.current_bill_number)\
                    .join(LegiscanSession, LegiscanBill.legiscan_session_id == LegiscanSession.id)\
                    .filter(
                        and_(
                            LegiscanSession.session_id == session_id,
                            LegiscanSession.state_code == state_code,
                            LegiscanBill.current_bill_number.in_(bill_numbers)
                        )
                    ).all()
                
                existing_bill_numbers = [bill.current_bill_number for bill in existing_bills]
                
                new_bills = [bill for bill in bill_numbers if bill not in existing_bill_numbers]
                
                logger.info(f"Found {len(new_bills)} new bills out of {len(bill_numbers)} total bills")
                return new_bills
                
        except Exception as e:
            logger.error(f"Error checking for existing bills: {str(e)}")
            raise

    @staticmethod
    async def process_new_bills():
        """
        Automated process to scrape, check, and submit new bills
        """
        logger.info("=== Starting bill processing job ===")
        try:
            logger.info("Step 1/5: Getting latest session ID for Iowa")
            session_id = SessionService.get_latest_session_id("IA")
            if not session_id:
                logger.error("Could not find latest session ID for Iowa")
                return
            logger.info(f"Found session ID: {session_id}")
            
            logger.info("Step 2/5: Checking API configuration")
            upvote_api_url = os.getenv('UPVOTE_API_BASE_URL')
            upvote_api_key = os.getenv('UPVOTE_API_KEY')
            if not upvote_api_url or not upvote_api_key:
                logger.error("UPVOTE_API configuration not found in environment")
                return
            logger.info("API configuration validated")
            
            logger.info("Step 3/5: Scraping bills from Iowa legislature website")
            bills = await BillService.scrape_bills()
            logger.info(f"Found {len(bills)} total bills")
            
            logger.info("Step 4/5: Checking for new bills")
            bill_numbers = [bill.bill_number for bill in bills]
            new_bills = await BillService.check_for_bills(
                bill_numbers,
                session_id,
                "IA"
            )
            
            if not new_bills:
                logger.info("No new bills found")
                return
            
            logger.info(f"Step 5/5: Submitting {len(new_bills)} new bills to Upvote API")
            endpoint = f"{upvote_api_url}/internal/bills?api_key={upvote_api_key}"
            success_count = 0
            error_count = 0
            
            async with aiohttp.ClientSession() as session:
                for bill_number in new_bills:
                    logger.info(f"Processing bill {bill_number}")
                    bill_data = next((b for b in bills if b.bill_number == bill_number), None)
                    if bill_data:
                        manual_entry = {
                            "bill": {
                                "state_code": "IA",
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
                                logger.info(f"Successfully submitted bill {bill_number}")
                        except Exception as e:
                            error_count += 1
                            logger.error(f"Error submitting bill {bill_number}: {str(e)}")

            await SlackService.notify_bill_processing(
                total_bills=len(bills),
                new_bills=[b for b in new_bills if b in [bill.bill_number for bill in bills]]
            )

            logger.info(f"=== Bill processing complete ===")
            logger.info(f"Summary: {success_count} bills submitted successfully, {error_count} failures")

        except Exception as e:
            logger.error(f"Error in automated bill processing: {str(e)}")
            raise