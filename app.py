import tornado.ioloop
import tornado.web
import json
from data import User, users

class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

class UsersHandler(MainHandler):
    def get(self):
        user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        self.write(json.dumps(user_data))

    def post(self):
        data = json.loads(self.request.body)
        new_id = max([user.id for user in users]) + 1
        new_user = User(new_id, data['username'], data['email'])
        users.append(new_user)
        self.write(json.dumps({'message': 'User added successfully'}))

class UserHandler(MainHandler):
    def get(self, user_id):
        user = next((user for user in users if user.id == int(user_id)), None)
        if user:
            self.write(json.dumps({'id': user.id, 'username': user.username, 'email': user.email}))
        else:
            self.set_status(404)
            self.write(json.dumps({'message': 'User not found'}))

    def put(self, user_id):
        data = json.loads(self.request.body)
        user = next((user for user in users if user.id == int(user_id)), None)
        if user:
            user.username = data['username']
            user.email = data['email']
            self.write(json.dumps({'message': 'User updated successfully'}))
        else:
            self.set_status(404)
            self.write(json.dumps({'message': 'User not found'}))

    def delete(self, user_id):
        global users
        users = [user for user in users if user.id != int(user_id)]
        self.write(json.dumps({'message': 'User deleted successfully'}))

def make_app():
    return tornado.web.Application([
        (r"/users", UsersHandler),
        (r"/users/(\d+)", UserHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on port 8888")
    tornado.ioloop.IOLoop.current().start()
