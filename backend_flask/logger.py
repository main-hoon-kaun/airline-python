import logging
import os

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure the logging system
logging.basicConfig(
    filename='logs/app.log',  # Log file will be created here
    level=logging.INFO,  # Log level set to INFO; change to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'  # Log message format
)

# Create a logger instance
airplane_logger = logging.getLogger("airplane") 
airport_logger = logging.getLogger("airport") 
flight_logger = logging.getLogger("flight") 
wallet_logger = logging.getLogger("wallet")
booking_logger = logging.getLogger("booking")