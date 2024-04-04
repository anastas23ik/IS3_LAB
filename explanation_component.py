

class ExplanationComponent:
    def get_logs(self, items):
        logs = ''
        for item in items:
            logs += str(item)
        return logs