import os
import urllib.request
from selenium.webdriver.common.by import By
from modules.selenium_wrapper import SeleniumWrapper
from modules.urls import *

class MathWS(SeleniumWrapper):
    """Downloads Reading worksheets from site"""
    def __init__(self, driver, grade):
        super().__init__(driver)
        self.subject = 'math'
        self.grade = grade

    def download(self):
        """Collects WS links and saves files"""
        self.initialize()
        links = self.get_links()
        self.save_files(links)
        self.driver.quit()

    def initialize(self):
        """Goes to math url for selected grade"""
        url = self.create_url()
        self.driver.get(url)

    def get_links(self):
        """Returns list of links for worksheets"""
        category_links = self.get_category_links()
        topic_links = self.get_topic_links(category_links)
        return self.get_ws_links(topic_links)

    def save_files(self, links):
        """Saves files associated with each pdf link"""    
        for link in links:
            if link:
                response = urllib.request.urlopen(link)
                filename = self.create_filename(link)
                with open(filename, 'wb') as file:
                    file.write(response.read())

    #Helper functions
    def create_url(self):
        """Creates url based on grade and subject"""
        return os.path.join(BASE_URL, SUBJECTS[self.subject], 
            GRADES[self.grade])

    def get_category_links(self):
        """Returns links for each Math category"""
        parent = self.driver.find_element(By.CLASS_NAME, 'content')
        a_tags = parent.find_elements(By.TAG_NAME, 'a')
        return [a_tag.get_attribute('href') for a_tag in a_tags]

    def get_topic_links(self, category_links):
        """Returns links for each topic"""
        topic_links = []
        for link in category_links[10:14]:
            if link:
                self.category = self.get_category(link)
                self.driver.get(link)
                parent = self.driver.find_element(By.CLASS_NAME, 'content')
                a_tags = parent.find_elements(By.TAG_NAME, 'a')
                links = [a_tag.get_attribute('href') for a_tag in a_tags]
                topic_links.extend(links)
        return topic_links

    def get_ws_links(self, topic_links):
        """Returns links for each ws"""
        ws_links = []
        for link in topic_links:
            if link:
                self.driver.get(link)
                a_tags = self.driver.find_elements(By.CLASS_NAME, 
                    'btn-worksheet')
                links = [a_tag.get_attribute('href') for a_tag in a_tags]
                ws_links.extend(links)
        return ws_links

    def get_category(self, link):
        """Returns category taken from link"""
        *_, category = link.split('/')
        return category

    def create_filename(self, link):
        """Creates filename based on grade and category"""
        *_, title = link.split('/')
        return os.path.join('pdfs', str(self.grade), self.subject, 
            self.category, title)