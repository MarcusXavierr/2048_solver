from selenium import webdriver
from time import sleep
from numpy import random
from src.keyboard import Keyboard
from src.helpers.game_helper import GameHelper

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# TODO: Usar alguma lib de flags pra ler as flags do usuário corretamente
# Primeiro eu vou botar só um delay
def main():
    driver.get("file:///home/marcus/Projects/courses/ufabc-ai/2048/external/play2048.co/index.html")
    gameHelper = GameHelper(driver)
    keyboard = Keyboard(driver)

    for i in range(1000):
        gameHelper.deal_with_paused_game(driver)
        keyboard.press_key(random.choice(keyboard.valid_keys))
        print(f'pressed key {i}')
        # Criar o helper de Delay inteligente
        sleep(0.1)

if __name__ == '__main__':
    main()
