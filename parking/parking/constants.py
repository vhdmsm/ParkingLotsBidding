from datetime import datetime

MIN_BID_VALUE = 49000  # Minimum allowed bid value to enter the auction
MAX_BID_VALUE = 700000  # Maximum allowd bid value
BID_STEP = 5  # Bids should be divisible by 5
AVAILABLE_PARKING_LOTS = 17  # Number of available spaces in the parking lot
END_TIME = datetime.fromtimestamp(1552901400)  # Ending time of auction in epoch
MIN_BID_DB_ID = 20000  # Dummy id of minimum bid object in the database
PARKING_CHANNEL_USERNAME = '@pegah_parking'