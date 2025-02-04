from app.services.bill_service import BillService
from app.services.session_service import SessionService
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_bill_existence():
    try:
        session_id = await SessionService.get_latest_session_id("IA")
        if not session_id:
            logger.error("Could not get latest session ID")
            return

        logger.info("Scraping bills...")
        bills = await BillService.scrape_bills()
        bill_numbers = [bill.bill_number for bill in bills]
        
        logger.info(f"Found {len(bill_numbers)} bills during scraping")
        
        logger.info("Checking bill existence in database...")
        new_bills = await BillService.check_for_bills(bill_numbers, session_id, "IA")
        
        print("\nResults:")
        print("-" * 50)
        for bill_number in bill_numbers:
            exists = bill_number not in new_bills
            status = "EXISTS" if exists else "MISSING"
            print(f"Bill {bill_number}: {status}")
        
        print("-" * 50)
        print(f"Total bills checked: {len(bill_numbers)}")
        print(f"Bills in database: {len(bill_numbers) - len(new_bills)}")
        print(f"Bills missing: {len(new_bills)}")

    except Exception as e:
        logger.error(f"Error during bill check: {str(e)}")
        logger.error(f"Error details: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_bill_existence())