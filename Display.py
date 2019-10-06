import curses
import logging


class Display(object):
    def __init__(self):
        self.__data_window = curses.newwin(
            curses.LINES - 2, curses.COLS - 1, 1, 0)
        self.__end_y, self.__end_x = self.__data_window.getmaxyx()
        self.__data_window.keypad(True)
        self.__title_window = curses.newwin(
            1, curses.COLS - 1, 0, 0)
        self.__title_window.keypad(True)

    def clear(self):
        self.__title_window.clear()
        self.__data_window.clear()

    def refresh(self):
        self.__title_window.refresh()
        self.__data_window.refresh()

    def draw_title(self, title):
        self.__title_window.addstr(0, 0, title, curses.A_BOLD)

    def draw_cursor(self, cursor_y, cursor_x):
        self.__data_window.move(cursor_y, cursor_x)
        self.__data_window.chgat(cursor_y, 0, self.__end_x, curses.A_REVERSE)

    def draw_data(self, data):
        if isinstance(data, dict):
            logging.debug("draw dict...")
            curr_line_to_write = 0
            for key, value in data.items():
                self.__data_window.addstr(curr_line_to_write, 0, '{}: {}'.format(key, value))
                curr_line_to_write += 1
                if curr_line_to_write >= self.__end_y:
                    break
        elif isinstance(data, list):
            curr_line_to_write = 0
            for element in data:
                self.__data_window.addstr(curr_line_to_write, 0, element)
                curr_line_to_write += 1
                if curr_line_to_write >= self.__end_y:
                    break
        else:
            self.__data_window.addstr(0, 0, data)
