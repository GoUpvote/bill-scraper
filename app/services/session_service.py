import logging

logger = logging.getLogger(__name__)

class SessionService:
    @staticmethod
    def get_latest_session_id(state_code: str) -> int:
        """
        Returns a hardcoded session ID for a given state.
        Since we are no longer using the database, we return 153.
        """
        logger.info(f"Using hardcoded session ID (153) for state {state_code}")
        return 153