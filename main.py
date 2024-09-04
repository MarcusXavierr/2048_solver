from selenium import webdriver
from core import Delay, Keyboard, Game
from utils import init_argparser
from utils import HTMLHelper

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

# TODO: Adicionar lib de .env pra ler os valures default do environment
def main():
    parser = init_argparser()
    args = parser.parse_args()
    sleeptime = args.delay

    driver.get("file:///home/marcus/Projects/courses/ufabc-ai/2048/external/play2048.co/index.html")
    gameHelper = Game(driver)
    htmlHelper = HTMLHelper(driver)
    keyboard = Keyboard(driver)
    delay = Delay()

    while True:
        delay.start_tracking()
        gameHelper.deal_with_paused_game(driver)
        move = gameHelper.get_best_next_move(htmlHelper.get_board_data())
        keyboard.press_key(move)
        delay.delay_with_compensation_ms(sleeptime)

if __name__ == '__main__':
    main()
