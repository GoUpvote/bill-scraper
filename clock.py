import asyncio
from apscheduler.schedulers.blocking import BlockingScheduler
from app.services.bill_service import BillService
import logging
from pytz import timezone
import sys
import traceback

# Configure logging to output to stdout with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

scheduler = BlockingScheduler()

async def process_bills():
    try:
        logger.info("Starting scheduled bill processing")
        await BillService.process_new_bills()
        logger.info("Completed scheduled bill processing")
    except Exception as e:
        logger.error(f"Error in scheduled bill processing: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

def run_process_bills():
    try:
        logger.info("Initiating process_bills run")
        asyncio.run(process_bills())
        logger.info("Completed process_bills run")
    except Exception as e:
        logger.error(f"Error in run_process_bills: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")

def start():
    try:
        logger.info("Starting scheduler")
        central = timezone('US/Central')
        
        # Morning window part 1 (7:30 AM - 7:59 AM)
        scheduler.add_job(
            run_process_bills,
            'cron',
            day_of_week='mon-thu',
            hour='7',
            minute='30-59/10',
            timezone=central
        )
        
        # Morning window part 2 (8:00 AM - 11:00 AM)
        scheduler.add_job(
            run_process_bills,
            'cron',
            day_of_week='mon-thu',
            hour='8-10',
            minute='*/10',
            timezone=central
        )
        
        # Early afternoon window (12:00 PM - 3:00 PM)
        scheduler.add_job(
            run_process_bills,
            'cron',
            day_of_week='mon-thu',
            hour='12-14',
            minute='*/10',
            timezone=central
        )
        
        # Late afternoon window (4:00 PM - 6:00 PM)
        scheduler.add_job(
            run_process_bills,
            'cron',
            day_of_week='mon-thu',
            hour='16-17',
            minute='*/10',
            timezone=central
        )

        logger.info("All jobs scheduled, starting scheduler...")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler shutting down...")
    except Exception as e:
        logger.error(f"Fatal error in scheduler: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

if __name__ == '__main__':
    try:
        logger.info("Initializing clock process")
        start()
    except Exception as e:
        logger.error(f"Fatal error in clock process: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)