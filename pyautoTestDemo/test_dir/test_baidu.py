import sys
sys.path.append("././page")
from time import sleep
from baidu_page import BaiduPage
from selenium import webdriver
import pytest

class TestBaidu():

    # @classmethod
    # def setup_class(cls):
    #     cls.driver = webdriver.Chrome()

    def baidu_search(self,browser,search_key):
        page = BaiduPage(browser)
        page.open()
        page.search_input(search_key)
        page.search_button()
        sleep(2)

    @pytest.mark.parametrize(
        "search_key",
        [("selenium"),
         ("ddt"),
         ("pytest")],
        ids=["case1","case2","case3"]
    )
    def test_baidu_search(self,browser,search_key):
        """百度搜索用例"""
        self.baidu_search(browser,search_key)
        assert browser.title == search_key + "_百度搜索"

    def test_baidu_search_case(self,browser):
        page = BaiduPage(browser)
        page.open()
        page.search_input("哈哈哈")
        page.search_button()
        sleep(2)
        self.assertEqual(page.get_title(),"selenium_百度搜索")

    # @classmethod
    # def teardown_class(cls):
    #     cls.driver.quit()