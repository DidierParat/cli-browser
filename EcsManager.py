import logging
import boto3


class EcsManager(object):
    def __init__(self, choice_handler, json_handler):
        self.__choice_handler = choice_handler
        self.__json_handler = json_handler
        self.__ecs_client = boto3.client('ecs')
        self.__initialize()
        self.__cluster = None

    def __initialize(self):
        data = self.__ecs_client.list_clusters()
        value, key = self.__extract_data_without_metadata(data)
        self.__json_handler.initialize(value, key)

    def update(self):
        next_data_requested = self.__json_handler.update()
        if next_data_requested:
            data, key = self.__get_data(next_data_requested)
            logging.debug('data: {}, key: {}'.format(data, key))
            if key:
                logging.debug("calling put_next_data")
                self.__json_handler.put_next_data(data, key)

    def __get_data(self, key):
        logging.debug('got request for data with key: {}'.format(key))
        data = None
        split_key = key.split('.')
        resource_arn = split_key[len(split_key) - 1]
        if 'clusterArns' in key:
            self.__cluster = resource_arn  # todo

            logging.debug('cluster: {}'.format(self.__cluster))
            choice = self.__choice_handler.get_choice(['services', 'tasks'])
            logging.debug('Choice made: {}'.format(choice))
            if choice == 'services':
                data = self.__ecs_client.list_services(cluster=self.__cluster, maxResults=100)
            elif choice == 'tasks':
                data = self.__ecs_client.list_tasks(cluster=self.__cluster)
        elif 'serviceArns' in key:
            data = self.__ecs_client.describe_services(cluster=self.__cluster, services=[resource_arn])
        elif 'taskDefinition' in key:
            data = self.__ecs_client.describe_task_definition(taskDefinition=resource_arn)
        elif 'taskArns' in key:
            data = self.__ecs_client.describe_tasks(cluster=self.__cluster, tasks=[resource_arn])
        return self.__extract_data_without_metadata(data)

    @staticmethod
    def __extract_data_without_metadata(data):
        if not data:
            return None, None
        for (key, value) in data.items():
            if key == 'failures':
                continue
            if key == 'ResponseMetadata':
                continue
            return value, key
