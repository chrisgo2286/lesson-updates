from venv import create
from modules.reading_ws import ReadingWS
from modules.math_ws import MathWS
from modules.selenium_wrapper import create_driver

driver = create_driver(headless=False)
ws = MathWS(driver, 3)
ws.download()