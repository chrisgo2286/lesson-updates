from venv import create
from modules.reading_ws import ReadingWS
from modules.selenium_wrapper import create_driver

driver = create_driver(headless=False)
ws = ReadingWS(driver, 3, 'exercises')
ws.download()