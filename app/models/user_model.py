from db_config import db_conn

class User:
    def __init__(self, name, surname, email, pwd, username, blocked=False, silenced=False, deleted=False, approved=False):
        self.name = name
        self.surname = surname
        self.email = email
        self.pwd = pwd
        self.username = username
        self.blocked = blocked
        self.silenced = silenced
        self.deleted = deleted
        self.approved = approved

    def create_user(self):
        user_data = {
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "pwd": self.pwd,
            "username": self.username,
            "blocked": self.blocked,
            "silenced": self.silenced,
            "deleted": self.deleted,
            "approved": self.approved,
        }
        
        filtered_user_data = {key: value for key, value in user_data.items() if value is not None and value != ""}

        db_conn.db.users.insert_one(filtered_user_data)

    def get_all():
        return list(db_conn.db.users.find())