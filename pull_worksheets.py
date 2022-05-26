import urllib.request
from venv import create
from selenium.webdriver.common.by import By
from modules.selenium_wrapper import SeleniumWrapper, create_driver

def download_file(url, filename):
    response = urllib.request.urlopen(url)
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()

url_leveled_stories = 'https://www.k5learning.com/reading-comprehension-worksheets/third-grade-3/leveled-reading-worksheets'
pdf_url = 'https://www.k5learning.com/worksheets/reading-comprehension'
filename = 'pdfs/test.pdf'

driver = create_driver(headless=False)

bot = SeleniumWrapper(driver)
bot.driver.get(url_leveled_stories)
table = bot.driver.find_element(By.CLASS_NAME, 'leveled-table')
rows = table.find_elements(By.TAG_NAME, 'tr')
links = []
for row in rows[1:]:
    a_tag = row.find_element(By.TAG_NAME, 'a')
    link = a_tag.get_attribute('href')
    links.append(link)
driver.quit()

for link in links:
    *_, title = link.split('/')
    driver = create_driver(headless=False)
    bot = SeleniumWrapper(driver)
    bot.driver.get(link)
    btn = bot.driver.find_element(By.CLASS_NAME, 'btn-worksheet')
    btn.click()
    url = bot.driver.current_url
    *_, title = url.split('/')
    download_file(f'{pdf_url}/{title}.pdf', f'pdfs/{title}.pdf')
    driver.quit()