from fastapi import APIRouter, HTTPException
from typing import List
import logging
from app.schemas.bill_schemas import BillResponse
from app.services.bill_service import BillService

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