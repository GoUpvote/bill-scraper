from sqlalchemy import desc
from app.database.session import get_db
from app.models import LegiscanSession
import logging
from app.database.config import settings

logger = logging.getLogger(__name__)

class SessionService:
    @staticmethod
    def get_latest_session_id(state_code: str) -> int:
        """
        Gets the most recent session ID for a given state
        
        Args:
            state_code: Two-letter state code (e.g., 'IA')
            
        Returns:
            int: The most recent session ID for the state
        """
        try:
            logger.info(f"Attempting to get session ID for {state_code}")
            
            with get_db() as db:
                latest_session = db.query(LegiscanSession)\
                    .filter(LegiscanSession.state_code == state_code)\
                    .order_by(desc(LegiscanSession.year_start))\
                    .first()
                
                if not latest_session:
                    logger.error(f"No session found for state {state_code}")
                    return None
                    
                logger.info(f"Found latest session ID {latest_session.session_id} for state {state_code}")
                return latest_session.session_id
                
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise