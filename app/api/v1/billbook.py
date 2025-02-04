from fastapi import APIRouter, HTTPException
from typing import List
import logging
from app.schemas.bill_schemas import BillResponse, BillCheckRequest, BillCheckResponse
from app.services.bill_service import BillService
from app.database.config import settings
from app.services.session_service import SessionService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/scrape-bills", response_model=List[BillResponse])
async def scrape_bills() -> List[BillResponse]:
    try:
        return await BillService.scrape_bills()
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/check-bills", response_model=BillCheckResponse)
async def check_bills(request: BillCheckRequest) -> BillCheckResponse:
    try:
        new_bills = await BillService.check_for_bills(
            request.bill_numbers,
            request.session_id,
            request.state_code
        )
        return BillCheckResponse(new_bill_numbers=new_bills)
    except Exception as e:
        error_msg = f"Error checking bills: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@router.post("/trigger-bill-processing")
async def trigger_bill_processing():
    """
    Manually trigger the bill processing job
    """
    try:
        logger.info("Manual trigger of bill processing initiated")
        await BillService.process_new_bills()
        return {"status": "success", "message": "Bill processing completed"}
    except Exception as e:
        error_msg = f"Error in manual bill processing: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)