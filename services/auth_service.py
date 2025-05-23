from models.user import User

class AuthService:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        if username in self.users:
            return False, "El usuario ya existe"
        self.users[username] = User(username, password)
        return True, "Usuario registrado correctamente"

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        return user and user.password == password
