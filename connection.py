
class Connection:
    def __init__(self, type, output, input):
        self.type = type
        self.output_node = output
        self.input_node = input

    def add_connection(self):
        self.output_node.add_connection(self)
        self.input_node.add_connection(self)
