from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

class Game:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def deal_with_paused_game(self, driver: WebDriver):
        won_the_game = driver.find_elements(By.CSS_SELECTOR, ".game-message.game-won")
        lose_the_game = driver.find_elements(By.CSS_SELECTOR, ".game-message.game-over")
        if len(won_the_game) == 0 and len(lose_the_game) == 0:
            return

        if len(lose_the_game) != 0:
            choice = input('1 - Tentar novamente\n2 - Parar\n')
            if choice == '2':
                exit()

            driver.find_element(By.CLASS_NAME, "retry-button").click()
            return

        # Win the game
        choice = input("1 - Continuar\n2 - Tentar novamente\n3 - Parar\n")
        if choice == '3':
            exit()

        if choice == '2':
            driver.find_element(By.CLASS_NAME, "retry-button").click()
            return

        driver.find_element(By.CLASS_NAME, "keep-playing-button").click()
        return

