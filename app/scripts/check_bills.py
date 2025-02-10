import asyncio
import logging
from app.services.bill_service import BillService
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_bill_existence():
    try:
        session_id = 937
        state_code = "IA"
        
        logger.info("Step 1/3: Scraping bills from Iowa legislature website")
        bills = await BillService.scrape_bills()
        bill_numbers = [bill.bill_number for bill in bills]
        logger.info(f"Found {len(bill_numbers)} bills during scraping")
        
        logger.info("Step 2/3: Checking bill existence via Upvote API")
        logger.info(f"Using API URL: {os.getenv('UPVOTE_API_BASE_URL')}")
        new_bills = await BillService.check_for_bills(bill_numbers, session_id, state_code)
        
        logger.info("Step 3/3: Generating report")
        print("\nResults:")
        print("-" * 50)
        for bill_number in bill_numbers:
            exists = bill_number not in new_bills
            status = "EXISTS" if exists else "MISSING"
            print(f"Bill {bill_number}: {status}")
        
        print("-" * 50)
        print(f"Total bills checked: {len(bill_numbers)}")
        print(f"Bills in Upvote: {len(bill_numbers) - len(new_bills)}")
        print(f"Bills missing from Upvote: {len(new_bills)}")

    except Exception as e:
        logger.error(f"Error during bill check: {str(e)}")
        logger.error(f"Error details: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_bill_existence())