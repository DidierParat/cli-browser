import logging
import re

from Action import Action


class JsonHandler(object):
    __PATH_DELIMITER = '.'

    def __init__(self, navigator):
        self.__navigator = navigator
        self.__curr_data = None
        self.__curr_path = ''
        self.__curr_title = ''
        self.__data_stack = []
        self.__path_stack = []
        self.__title_stack = []

    def initialize(self, data, title):
        self.__curr_data = data
        self.__curr_path = ''
        self.__curr_title = title
        self.__data_stack.append(self.__curr_data)
        self.__path_stack.append(self.__curr_path)
        self.__title_stack.append(self.__curr_title)

    def __pop_previous_data(self):
        if self.__data_stack:
            self.__curr_data = self.__data_stack.pop()
            self.__curr_path = self.__path_stack.pop()
            self.__curr_title = self.__title_stack.pop()

    def put_next_data(self, data, key):
        self.__data_stack.append(self.__curr_data)
        self.__path_stack.append(self.__curr_path)
        self.__title_stack.append(self.__curr_title)
        self.__curr_data = data
        self.__curr_path = ''
        self.__curr_title = key

    def update(self):
        self.__navigator.set_cursor(0)
        action = None
        cursor_y = None
        data_to_draw = self.__compute_data_to_draw()
        title_to_draw = self.__compute_title_to_draw()
        logging.debug('data_to_draw: {}'.format(data_to_draw))
        while not action:
            action, cursor_y = self.__navigator.update(data_to_draw, title_to_draw)
        if action == Action.GET_NEXT_ELEMENT:
            self.__update_path_with_next_element(cursor_y, data_to_draw)
            return self.__get_key_for_new_data()
        elif action == Action.GET_PREVIOUS_ELEMENT:
            self.__update_path_with_previous_element()
        return None

    def __compute_title_to_draw(self):
        return self.__curr_title + '->' + self.__curr_path

    def __compute_data_to_draw(self):
        current_element = self.__get_current_element()
        logging.debug('current_element: {}'.format(current_element))
        if isinstance(current_element, dict):
            value_to_return = {}
            for (key, value) in current_element.items():
                value_to_return[key] = self.__compute_element(value)
            return value_to_return
        if isinstance(current_element, list):
            value_to_return = []
            for value in current_element:
                value_to_return.append(self.__compute_element(value))
            return value_to_return
        return current_element

    @staticmethod
    def __compute_element(value):
        if isinstance(value, list):
            return '[...]'
        elif isinstance(value, dict):
            return '{...}'
        else:
            return value

    def __get_key_for_new_data(self):
        current_element = self.__get_current_element()
        if not current_element:
            return None
        if self.is_simple_element(current_element):
            return self.__curr_title + self.__PATH_DELIMITER + self.__curr_path + self.__PATH_DELIMITER + current_element
        return None

    def __update_path_with_next_element(self, cursor_y, data_drawn):
        if isinstance(data_drawn, dict):
            logging.debug('self.__curr_element is a dict')
            i = 0
            for key, value in data_drawn.items():
                if i >= cursor_y:
                    self.__curr_path += self.__PATH_DELIMITER + key
                    break
                i += 1
        elif isinstance(data_drawn, list):
            logging.debug('self.__curr_element is a list')
            self.__curr_path += '{}[{}]'.format(self.__PATH_DELIMITER, cursor_y)

    def __update_path_with_previous_element(self):
        logging.debug('updating path, before: {}'.format(self.__curr_path))
        split_path = self.__curr_path.split(self.__PATH_DELIMITER)
        logging.debug(split_path)
        if len(split_path) == 1:
            self.__pop_previous_data()
        else:
            self.__curr_path = split_path[0]
            for i in range(1, len(split_path) - 1):
                self.__curr_path += self.__PATH_DELIMITER + split_path[i]
        logging.debug('updating path, after: {}'.format(self.__curr_path))

    @staticmethod
    def is_simple_element(element):
        return not isinstance(element, dict) and not isinstance(element, list)

    def __get_current_element(self):
        current_element = self.__curr_data
        split_path = self.__curr_path.split(self.__PATH_DELIMITER)
        logging.debug('split_path: {}'.format(split_path))
        for i in range(1, len(split_path)):
            logging.debug('split_path[i]: {}'.format(split_path[i]))
            index_search = re.search('\[([0-9])\]', split_path[i])
            if index_search:
                index = int(index_search.group(1))
                logging.debug('index: {}'.format(index))
                current_element = current_element[index]
            elif isinstance(current_element, dict):
                current_element = current_element.get(split_path[i])
        return current_element
