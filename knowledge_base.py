import json
from connection import Connection
from node import Node


class KnowledgeBase:
    def __init__(self):
        self.list_nodes = []
        self.load()

    # загружаем json файл, парсим его и наполняем базу знаний
    def load(self):
        with open('./semantic_web.json', 'r', -1, 'utf8') as file:
            data = json.load(file)

        # сначала проходим по всем узлам, и устанавливаем их
        for node in data:
            self.list_nodes.append(Node(node.get('value')))

        # далее, снова проходим по узлам, и устанавливаем связи, исходящие от этих узлов
        for node in data:
            value = node.get('value')
            connections = node.get('connections')
            from_node = self.find_node(value)

            if from_node != None and connections != None:
                for connection in connections:
                    type = connection.get('type')
                    to_node = self.find_node(connection.get('to_node'))
                    Connection(type, to_node, from_node).add_connection()

    # метод для фильтрации списка по уникальным значениям
    def get_unique_list(self, list):
        unique = []
        for node in list:
            try:
                unique.index(node) >= 0
            except:
                unique.append(node)
        return unique

    # метод для поиска узла по его значению
    def find_node(self, node_name):
        for node in self.list_nodes:
            if node.name == node_name:
                return node

    # метод для поиска узлов, соединенных каким-либо отношением с указанным узлом
    # если указан connection_type, то возвращаем узлы с указанным типом связи
    # если не указан, то возвращаем все узлы вне зависимости от типа связи
    def find_nodes_by_output(self, output_name, connection_type=None):
        nodes = []
        for node in self.list_nodes:
            if node.connections and len(node.connections) > 0:
                for connection in node.connections:
                    if connection.output_node.name == output_name:
                        if connection_type == None or connection_type == connection.type:
                            nodes.append(connection.input_node)
        return self.get_unique_list(nodes)

    # метод для поиска указанной связи в параметре connection_type
    # если параметр node_type равен 'input', то возвращаем те узлы, от которых идет связь
    # если параметр node_type равен 'output', то возвращаем те узлы, к которым идет связь
    def find_nodes_by_connection(self, connection_type, node_type):
        nodes = []
        for node in self.list_nodes:
            if node.connections and len(node.connections) > 0:
                for connection in node.connections:
                    if connection.type == connection_type:
                        if node_type == 'input':
                            nodes.append(connection.output_node)
                        elif node_type == 'output':
                            nodes.append(connection.input_node)
        return self.get_unique_list(nodes)