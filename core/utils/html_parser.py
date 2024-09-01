from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


class HTMLHelper:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

