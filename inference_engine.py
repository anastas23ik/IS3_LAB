class InferenceEngine:
    def __init__(self, nodes):
        self.nodes = nodes
        self.used = []

    # поиск узла по имени
    def find_node_by_name(self, name):
        for node in self.nodes:
            if node.name == name:
                return node

    def add_combination_used(self, connection, node_name):
        self.used.append(f'connection: {connection} \n')
        self.used.append(f'node: {node_name} \n')

    # обработка запроса, касающегося бюджета
    def budget_request(self, pet):
        pet_node = self.find_node_by_name(pet)

        self.used.append(f'node: {pet_node.name} \n')
        success_nodes = []
        for connection in pet_node.connections:
            if connection.type == 'requires':
                self.used.append(f'connection: requires \n')
                self.used.append(f'node: {connection.output_node.name} \n')
                success_nodes.append(connection.output_node.name)

        return success_nodes

    # обработка запроса, касающегося характеристик питомца
    def pet_characteristic_request(self, pet, characteristic):
        char_node = self.find_node_by_name(characteristic)
        pet_node = self.find_node_by_name(pet)

        self.used.append(f'node: {pet_node.name} \n')
        self.used.append(f'node: {char_node.name} \n')

        for connection in char_node.connections:
            if connection.type == 'has-characteristic':
                if connection.input_node.name == pet:
                    self.add_combination_used('has-characteristic', connection.input_node.name)
                    self.used.append('Да \n')
                    return "Да"
            elif connection.type == 'is-need':
                if connection.input_node.name == pet:
                    self.add_combination_used('is-need', connection.input_node.name)
                    self.used.append('Да \n')
                    return "Да"
            elif connection.type == 'requires':
                if connection.input_node.name == pet:
                    self.add_combination_used('requires', connection.input_node.name)
                    self.used.append('Да \n')
                    return "Да"

        self.used.append('Нет \n')
        return "Нет"

    # обработка запроса, касающегося требований к питомцу
    def requirements_request(self, requirement_general, requirement_individual):
        req_gen_node = self.find_node_by_name(requirement_general)
        req_ind_node = self.find_node_by_name(requirement_individual)

        self.used.append(f'node: {req_gen_node.name} \n')
        self.used.append(f'node: {req_ind_node.name} \n')

        for connection in req_gen_node.connections:
            if connection.type == 'IS-A':
                if connection.input_node.name == requirement_individual:
                    self.add_combination_used('IS-A', connection.input_node.name)
                    self.used.append('Да \n')
                    return "Да"

        self.used.append('Нет \n')
        return "Нет"