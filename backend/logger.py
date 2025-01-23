import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file
        logging.StreamHandler()  # Logs to console
    ]
)

# Create a logger instance
logger = logging.getLogger("BackendLogger")

# Example usage
def process_request(data):
    try:
        logger.info("Processing request with data: %s", data)
        if not data:
            raise ValueError("Invalid data provided")
        # Process data
        logger.debug("Data processed successfully")
    except ValueError as e:
        logger.error("An error occurred: %s", e)
    except Exception as e:
        logger.critical("Unexpected error: %s", e)

# Call the function
process_request({"key": "value"})  # Example with valid data
process_request(None)  # Example with invalid data
