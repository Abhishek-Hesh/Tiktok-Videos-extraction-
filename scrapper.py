import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
from selenium.webdriver import ChromeOptions
import urllib

BASE_URL = 'https://www.tiktok.com/'

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': r'C:\Users\Abhishek Hesh\Downloads\ExtractedVideos',
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True}
chrome_options.add_experimental_option('prefs', prefs)

class Process(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\SeleniumDrivers", teardown=False, chrome_options=chrome_options):
        self.driver_path = driver_path
        self.teardown = teardown
        self.titles = []
        self.links = []
        self.download_dir = 'C:/Users/Abhishek Hesh/Downloads/ExtractedVideos'
        self.url = None
        self.data = None
        os.environ['PATH'] += ";"+self.driver_path
        super(Process, self).__init__(options=chrome_options)
        self.implicitly_wait(5)
        self.maximize_window()
        
    def __exit__(self, *args):
        if self.teardown:
            self.quit()
    
    def load_account(self, account_name):
#         self.implicitly_wait(5)
#         self.refresh()
#         self.refresh()
#         sleep(10)
        #-----------------------------------------
        try:
            self.url = BASE_URL + '@' + account_name
            self.get(self.url)
            element_present = EC.presence_of_element_located((By.TAG_NAME, "body"))
            WebDriverWait(self, 10).until(element_present)
            print("Page loaded successfully!")
        except TimeoutError:
            print("Page not loaded within the specified time.")

        
    def video_page(self):
        sleep(10)
        video = self.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div/a")
        # /html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/div/div/a /html/body/div[1]/div[2]/div[2]/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div/a
        self.implicitly_wait(5)
        video.click()
        self.implicitly_wait(10)
    
    
    def collect_links(self, links=1):
        count = links
        while count != 0:
            try:
                link = self.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/p")
                title = self.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/div[4]/div/div[2]/div[1]/div/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/span[1]") 
                print(title.text, str(link.text).split("?")[0])
                sleep(10)
                count -= 1
                self.links.append(str(link.text).split("?")[0])
                title = "_".join(title.text.split(' '[:len(title.text.split())]))
                self.titles.append(title[:len(title)-1])
                down = self.find_element(by=By.XPATH, value=f"/html/body/div[1]/div[2]/div[4]/div/div[1]/button[3]")
                down.click()
            except Exception as e:
                sleep(30)
        self.data = {'title':self.titles, 'link':self.links}
#         if len(self.titles) == links:
#             self.quit()

    def process(self, account_name, links=1):
        self.load_account(account_name)
        sleep(20)
        self.video_page()
        sleep(5)
        self.collect_links(links=links)
    
    def downloader(self):
        directory_path = r'C:\Users\Abhishek Hesh\Downloads\ExtractedVideos'
        if os.path.exists(directory_path):
            print(f"The directory '{directory_path}' exists.")
        else:
            os.makedirs(self.download_dir)
            print(f"The directory '{directory_path}' has been created.")
        self.url = 'https://ssstik.io/en'
        self.implicitly_wait(5)
        titles = self.data['title']
        links = self.data['link']
        for i, j in zip(titles, links):
            self.get(self.url)
            inputd = self.find_element(by=By.CSS_SELECTOR, value='#main_page_text')
            self.implicitly_wait(10)
            self.execute_script("arguments[0].style.visibility = 'visible';", inputd)
            self.implicitly_wait(10)
            sleep(10)
            if inputd.is_enabled():
                print('Done')
                inputd.send_keys(j)
                downloadButton = self.find_element(by=By.CSS_SELECTOR, value='#submit')
                downloadButton.click()
                sleep(5)
                watermarkButton = self.find_element(by=By.XPATH, value=f'/html/body/main/section[1]/div/div/div[3]/div/div/div[2]/a[1]')
                watermarkButton.click()
                sleep(10)
            else:
                print('not Done')
                
    def rename(self):
        files = os.listdir(self.download_dir)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.download_dir, x)), reverse=True)
        titles = self.data['title']
        for file, title in zip(files, titles):
            
            file_name = title + '.mp4'
            old_file_path = os.path.join(self.download_dir, file)
            new_file_path = os.path.join(self.download_dir, file_name)
            os.rename(old_file_path, new_file_path)