class APIException(Exception):

    def __init__(self, *args: object, response=None) -> None:
        super(APIException, self).__init__(*args)
        self.response = response
