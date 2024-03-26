import time
from selenium.webdriver.common.by import By
class BasePage:
    '''基础Page层，封装一些常用方法'''
    def __init__(self,browser):
        self.browser = browser
    def open(self,url=None):
        if url is None:
            self.browser.get(self.url)
        else:
            self.browser.get(url)
    def by_id(self,id_):
        return self.browser.find_element(By.ID, id_)
    def get_title(self):
        return self.browser.title
    def by_css(self,css):
        return self.browser.find_element(By.CSS_SELECTOR, css)
    def by_link_text(self,link_text_):
        return self.browser.find_element(By.LINK_TEXT, link_text_)