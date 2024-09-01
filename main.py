from selenium import webdriver
from numpy import random
from core import Delay, Keyboard, Game

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# TODO: Usar alguma lib de flags pra ler as flags do usuário corretamente
# Primeiro eu vou botar só um delay
def main():
    driver.get("file:///home/marcus/Projects/courses/ufabc-ai/2048/external/play2048.co/index.html")
    gameHelper = Game(driver)
    keyboard = Keyboard(driver)
    delay = Delay()

    for _ in range(1000):
        delay.start_tracking()
        gameHelper.deal_with_paused_game(driver)
        # Here the desition is made
        keyboard.press_key(random.choice(keyboard.valid_keys))
        delay.delay_with_compensation_ms(150)

if __name__ == '__main__':
    main()
