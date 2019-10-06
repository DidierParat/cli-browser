import curses
import logging

from Action import Action


class Navigator(object):
    def __init__(self, display):
        self.__input_window = curses.newwin(
            1, curses.COLS - 1, curses.LINES - 1, 0)
        self.__input_window.keypad(True)
        self.__display = display
        self.__curr_y = 0
        self.__curr_x = 0

    def update(self, data, title):
        logging.debug('navigator.update')
        self.__display.clear()
        self.__display.draw_title(title)
        self.__display.draw_data(data)
        self.__display.draw_cursor(self.__curr_y, self.__curr_x)
        self.__display.refresh()
        key_pressed = self.__input_window.getkey()
        return self.__do_next_action(data, key_pressed), self.__curr_y

    def set_cursor(self, cursor_y):
        self.__curr_y = cursor_y

    def __do_next_action(self, data, key_pressed):
        logging.debug('key pressed: {}'.format(key_pressed))
        if key_pressed == 'KEY_UP' and self.__curr_y != 0:
            self.__curr_y = self.__curr_y - 1
        elif key_pressed == 'KEY_DOWN' and self.__curr_y < len(data) - 1:
            self.__curr_y = self.__curr_y + 1
        elif key_pressed == 'KEY_RIGHT':
            return Action.GET_NEXT_ELEMENT
        elif key_pressed == 'KEY_LEFT':
            return Action.GET_PREVIOUS_ELEMENT
        elif key_pressed == '\n':
            self.__input_window.clear()
            curses.echo()
            search_word = self.__input_window.getstr()
            curses.noecho()
            logging.debug('you want to search for: {}'.format(search_word))
        return None
