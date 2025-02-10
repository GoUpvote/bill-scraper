import logging
from app.database.session import get_db
from app.models import LegiscanBill  # Ensure this model has bill_number and state_code attributes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    with get_db() as db:
        # Query bills with bill_number 'hf207' (case-insensitive) and state 'IA'
        bills = db.query(LegiscanBill).filter(
            LegiscanBill.readable_bill_number.ilike("hf207"),
            LegiscanBill.state_code == "IA"
        ).all()

        if not bills:
            logger.info("No bills found with bill_number 'hf207' for state IA.")
        else:
            for bill in bills:
                logger.info("Bill Information:")
                # Exclude internal SQLAlchemy state attribute
                for key, value in bill.__dict__.items():
                    if key != "_sa_instance_state":
                        logger.info(f"{key}: {value}")
                logger.info("-" * 40)

if __name__ == "__main__":
    main() 