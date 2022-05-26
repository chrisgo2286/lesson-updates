from optparse import Option
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SeleniumWrapper:
	DELAY = 1.5
	def __init__(self, driver):
		self.driver = driver
		self.duration = 30 #Change to 60 in production
		self.wait = WebDriverWait(self.driver, self.duration)

# CLICKER FUNCTIONS
	def click_link_text(self, element):
		"""Waits until element is clickable"""
		self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.LINK_TEXT, element).click()

	def click_name(self, element):
		"""Waits until element is clickable"""
		self.wait.until(EC.element_to_be_clickable((By.NAME, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.NAME, element).click()

	def click_id(self, element):
		"""Waits until element is clickable"""
		self.wait.until(EC.element_to_be_clickable((By.ID, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.ID, element).click()

	def click_xpath(self, element):
		"""Waits until element is clickable"""
		self.wait.until(EC.element_to_be_clickable((By.XPATH, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.XPATH, element).click()

# WAIT FUNCTIONS

	def wait_by_link_text(self, element):
		self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT, element)))
		time.sleep(self.DELAY)
	
	def wait_by_name(self, element):
		self.wait.until(EC.visibility_of_element_located((By.NAME, element)))
		time.sleep(self.DELAY)

	def wait_by_id(self, element):
		self.wait.until(EC.visibility_of_element_located((By.ID, element)))
		time.sleep(self.DELAY)

	def wait_by_xpath(self, element):
		self.wait.until(EC.visibility_of_element_located((By.XPATH, element)))
		time.sleep(self.DELAY)

# SEND KEY FUNCTIONS

	def send_keys_by_name(self, element, text):
		self.wait.until(EC.element_to_be_clickable((By.NAME, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.NAME, element).send_keys(text)

	def send_keys_by_id(self, element, text):
		self.wait.until(EC.element_to_be_clickable((By.ID, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.ID, element).send_keys(text)

	def send_keys_by_xpath(self, element, text):
		self.wait.until(EC.element_to_be_clickable((By.XPATH, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.XPATH, element).send_keys(text)

# SELECT VALUE FUNCTIONS

	def select_value_by_name(self, element, value):
		self.wait.until(EC.element_to_be_clickable((By.NAME, element)))
		time.sleep(self.DELAY)
		Select(self.driver.find_element(By.NAME, element)).select_by_value(value)

	def select_value_by_id(self, element, value):
		self.wait.until(EC.element_to_be_clickable((By.ID, element)))
		time.sleep(self.DELAY)
		Select(self.driver.find_element(By.ID, element)).select_by_value(value)

	def select_text_by_id(self, element, value):
		self.wait.until(EC.element_to_be_clickable((By.ID, element)))
		time.sleep(self.DELAY)
		Select(self.driver.find_element(By.ID, element)).\
			select_by_visible_text(value)

# CLEAR FUNCTIONS

	def clear_by_id(self, element):
		self.wait.until(EC.element_to_be_clickable((By.ID, element)))
		time.sleep(self.DELAY)
		self.driver.find_element(By.ID, element).clear()

# WAIT FOR INVISIBLE FUNCTIONS
	
	def wait_for_invisibility_by_id(self, element):
		self.wait.until(EC.invisibility_of_element_located((By.ID, element)))

# WINDOW FUNCTIONS
	def manage_pop_up(self):
		"""returns main and browse page"""
		# self.wait_for_new_window()
		main_page = self.driver.window_handles[0] #Is main page always 0 index?
		pop_up = self.driver.window_handles[1]
		return main_page, pop_up

# MISC FUNCTIONS

	def accept_alert(self):
		"""Waits for alert and accepts it"""
		try:
			self.wait.until(EC.alert_is_present(), 'No alert present!')
			time.sleep(self.DELAY)
			self.driver.switch_to.alert.accept()
		except:
			pass

	def switch_frames(self,frames):
		"""Switches to default frame then cycles through list of frames"""
		self.driver.switch_to.default_content()
		for frame in frames:
			self.wait_by_name(frame)
			self.driver.switch_to.frame(self.driver.find_element(By.NAME, frame))

def create_driver(headless=True):
	"""Returns webdriver"""
	options = config_options() if headless else None
	driver = webdriver.Firefox(options=options)
	driver.implicitly_wait(30)
	return driver

def config_options():
	"""Return options for headless webdriver"""	
	options = Options()
	options.headless = True
	return options
