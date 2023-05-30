class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get(username):
        doc = db.get(username)
        if doc:
            return User(doc['username'], doc['password'])
        return None

    def save(self):
        doc = {'_id': self.username, 'username': self.username, 'password': self.password}
        db.save(doc)