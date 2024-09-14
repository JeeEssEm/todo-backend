class Response:
    def __init__(self, message=None, **data):
        self.body = {
            'detail': message,
            'content': data
        }
