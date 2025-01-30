from pydantic import BaseModel

class BillResponse(BaseModel):
    bill_number: str
    base64_html: str