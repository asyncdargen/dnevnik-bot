class Credentials:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def __iter__(self):
        return iter([self.login, self.password])
