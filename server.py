from flask_app.controllers import browse_projects, browse_users, messages, roles, cities, feed, my_projects, edit_users
from flask_app import app

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port = 8800)