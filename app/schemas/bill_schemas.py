from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class BillResponse(BaseModel):
    bill_number: str
    bill_title: Optional[str] = None
    base64_html: str
    state_link: str

class ManualBillEntry(BaseModel):
    state_code: str
    bill_number: str
    current_state: str
    introduced_date: str
    state_link: str
    bill_text_data_base64: str

class BillCheckRequest(BaseModel):
    bill_numbers: List[str]
    session_id: int
    state_code: str

class BillCheckResponse(BaseModel):
    new_bill_numbers: List[str]