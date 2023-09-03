from db_config import db_conn

class Stream:
    def __init__(self, title, created_on=None, summary=None, exp_method=None, iso_sens=None, location=None, country=None, deleted=False, user_id=None):
        self.title = title
        self.created_on = created_on
        self.summary = summary
        self.exp_method = exp_method
        self.iso_sens = iso_sens
        self.location = location
        self.country = country
        self.deleted = deleted
        self.user_id = user_id

    def create_stream(self):
        stream_data = {
            "title": self.title,
            "created_on": self.created_on,
            "summary": self.summary,
            "exp_method": self.exp_method,
            "iso_sens": self.iso_sens,
            "location": self.location,
            "country": self.country,
            "deleted": self.deleted,
            "user_id": self.user_id,
        }
        
        filtered_stream_data = {key: value for key, value in stream_data.items() if value is not None and value != ""}
        
        db_conn.db.streams.insert_one(filtered_stream_data)