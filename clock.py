import asyncio
from apscheduler.schedulers.blocking import BlockingScheduler
from app.services.bill_service import BillService
import logging

logger = logging.getLogger(__name__)
scheduler = BlockingScheduler()

async def process_bills():
    try:
        logger.info("Starting scheduled bill processing")
        await BillService.process_new_bills()
        logger.info("Completed scheduled bill processing")
    except Exception as e:
        logger.error(f"Error in scheduled bill processing: {str(e)}")

def run_process_bills():
    asyncio.run(process_bills())

def start():
    scheduler.add_job(run_process_bills, 'interval', minutes=15)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    start()