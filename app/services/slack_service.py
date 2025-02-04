import aiohttp
import os
import logging
from typing import List

logger = logging.getLogger(__name__)

class SlackService:
    @staticmethod
    async def notify_bill_processing(total_bills: int, new_bills: List[str]):
        """
        Send a Slack notification about bill processing results
        """
        webhook_url = os.getenv('SLACK_WEBHOOK_URL')
        if not webhook_url:
            logger.error("SLACK_WEBHOOK_URL not configured")
            return

        try:
            message = f"IA Bill Scraper Execution Complete\n"
            message += f"Total Bills Scanned: {total_bills}\n"
            message += f"New Bills Found: {len(new_bills)}\n"
            
            if new_bills:
                message += "\nNew Bills:\n"
                message += "\n".join([f"• {bill}" for bill in new_bills])

            async with aiohttp.ClientSession() as session:
                await session.post(
                    webhook_url,
                    json={"text": message},
                    headers={"Content-Type": "application/json"}
                )
            logger.info("Slack notification sent successfully")
        except Exception as e:
            logger.error(f"Error sending Slack notification: {str(e)}") 