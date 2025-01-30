import base64
import logging
import aiohttp
from bs4 import BeautifulSoup
import asyncio
from typing import List, Optional
from app.schemas.bill_schemas import BillResponse
from app.utils.http_utils import DEFAULT_HEADERS, get_bill_headers

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
    async def process_bill_results(bills_data: list, bill_numbers: list, results: list) -> List[BillResponse]:
        for bill_number, html_content in zip(bill_numbers, results):
            if html_content:
                bills_data.append(BillResponse(
                    bill_number=bill_number,
                    base64_html=BillService.convert_to_base64(html_content)
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
                    for link in bill_links:
                        bill_number = link.text.strip().replace(" ", "")
                        bill_numbers.append(bill_number)
                        tasks.append(BillService.get_bill_html(session, bill_number))
                    
                    results = await asyncio.gather(*tasks)
                    bills_data = await BillService.process_bill_results([], bill_numbers, results)
            
            logger.info(f"Scraping complete. Successfully processed {len(bills_data)} bills")
            return bills_data
                    
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise