import os

CODES_FILE = "codes.txt"
if not os.path.exists(CODES_FILE):
    with open(CODES_FILE, "w", encoding="UTF-8") as f:
        pass

DEFAULT_EVENT_TIMEOUT = 1000000
