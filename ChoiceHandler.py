import curses
import logging

from Action import Action


class ChoiceHandler(object):
    __CHOICES_TITLE = 'What are you looking for?'

    def __init__(self, navigator):
        self.__navigator = navigator

    def get_choice(self, choices):
        self.__navigator.set_cursor(0)
        action = None
        cursor_y = None
        while not action:
            action, cursor_y = self.__navigator.update(choices, self.__CHOICES_TITLE)
        logging.debug('action: {}'.format(action))
        logging.debug('cursor_y: {}'.format(cursor_y))
        if action == Action.GET_PREVIOUS_ELEMENT:
            return None
        elif action == Action.GET_NEXT_ELEMENT:
            logging.debug('choices: {}'.format(choices))
            logging.debug('cursor_y: {}'.format(cursor_y))
            return choices[cursor_y]
