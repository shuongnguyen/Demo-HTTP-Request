class User:
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

users = [
    User(1, "user1", "user1@example.com"),
    User(2, "user2", "user2@example.com")
]
