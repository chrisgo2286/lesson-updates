import os
import urllib.request
from selenium.webdriver.common.by import By
from modules.selenium_wrapper import SeleniumWrapper
from modules.urls import *

class ReadingWS(SeleniumWrapper):
    """Downloads Reading worksheets from site"""
    def __init__(self, driver, grade, topic):
        super().__init__(driver)
        self.subject = 'reading'
        self.grade = grade
        self.topic = topic
        self.link_funcs = {
            'leveled_stories': self.get_leveled_stories_links,
            'childrens_stories': self.get_childrens_stories_or_fables_links,
            'fables': self.get_childrens_stories_or_fables_links,
            'exercises': self.get_exercises_links,
        }

    def download(self):
        """Calls get link functions based on topic and downloads worksheets"""
        self.initialize()
        links = self.link_funcs[self.topic]()
        print(links)
        self.save_files(links)
        self.driver.quit()

    def initialize(self):
        url = self.create_url(self.topic)
        self.driver.get(url)

    def get_leveled_stories_links(self):
        """Returns links for leveled stories"""
        parent = self.driver.find_element(By.CLASS_NAME, 'leveled-table')
        children = parent.find_elements(By.TAG_NAME, 'tr')[1:]
        a_tags = [child.find_element(By.TAG_NAME, 'a') for child in children]
        return [a_tag.get_attribute('href') for a_tag in a_tags]

    def get_childrens_stories_or_fables_links(self):
        """Gets links for childrens stories"""
        parent = self.driver.find_element(By.CLASS_NAME, 'additional-text')
        a_tags = parent.find_elements(By.TAG_NAME, 'a')        
        return [a_tag.get_attribute('href') for a_tag in a_tags]

    def get_exercises_links(self):
        """Gets links for reading comprehension exercises"""
        parent = self.driver.find_element(By.CLASS_NAME, 'content')
        a_tags = parent.find_elements(By.TAG_NAME, 'a')        
        links = [a_tag.get_attribute('href') for a_tag in a_tags]
        sublinks = []
        for link in links:
            if link != None:
                sublinks.extend(self.get_exercises_sublinks(link))
        return sublinks

    def save_files(self, links):
        """Saves files associated with each pdf link"""    
        for link in links:
            if self.topic != 'exercises':
                link = self.find_url(link)
            response = urllib.request.urlopen(link)
            filename = self.create_filename(link)
            with open(filename, 'wb') as file:
                file.write(response.read())

    # Helper Functions
    
    def create_url(self, topic):
        """Creates url based on topic and grade"""
        return os.path.join(BASE_URL, SUBJECTS[self.subject], 
            GRADES[self.grade], TOPICS[self.topic])

    def get_exercises_sublinks(self, link):
        """Gets sublinks for reading comprehension exercises"""
        self.driver.get(link)
        a_tags = self.driver.find_elements(By.CLASS_NAME, 'btn-worksheet')
        links = [a_tag.get_attribute('href') for a_tag in a_tags]
        return links

    def find_url(self, link):
        """Returns url of pdf"""
        self.driver.get(link)
        btn = self.driver.find_element(By.CLASS_NAME, 'btn-worksheet')
        return btn.get_attribute('href')

    def create_filename(self, url):
        """Creates filename based on grade, subject, url"""
        *_, title = url.split('/')
        return os.path.join('pdfs', str(self.grade), self.subject, self.topic,
            f'{title}.pdf')