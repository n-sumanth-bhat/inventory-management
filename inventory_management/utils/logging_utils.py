import logging

logger = logging.getLogger('inventory')

def log_request(user, action, result):
    logger.debug(f"User: {user} | Action: {action} | Result: {result}")
