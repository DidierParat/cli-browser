import logging
from curses import wrapper

from ChoiceHandler import ChoiceHandler
from EcsManager import EcsManager
from Display import Display
from JsonHandler import JsonHandler
from Navigator import Navigator


def main(stdscr):
    logging.basicConfig(
        level=logging.DEBUG,
        filename='app.log',
        filemode='w',
        format='%(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s')
    print('Initializing...')
    display = Display()
    navigator = Navigator(display)
    choice_handler = ChoiceHandler(navigator)
    json_handler = JsonHandler(navigator)
    data_handler = EcsManager(choice_handler, json_handler)
    while True:
        data_handler.update()


wrapper(main)
