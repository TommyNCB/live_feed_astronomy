from db_config import db_conn
from bson import ObjectId

post_dict = {}

class Post:
    def __init__(self, title, type=None, created_on=None, summary=None, user_id=None):
        self.title = title
        self.created_on = created_on
        self.summary = summary
        self.type = type
        self.user_id = user_id

    def create_post(self):
        post_data = {
            "title": self.title,
            "type": self.type,
            "created_on": self.created_on,
            "summary": self.summary,
            "user_id": self.user_id,
        }

        filtered_post_data = {key: value for key, value in post_data.items() if value is not None and value != ""}
        
        results = db_conn.db.posts.insert_one(filtered_post_data)
        
        return results.inserted_id
    
    def get_post_title_by_id(post_id):
        post_id_obj = ObjectId(post_id)
        post = db_conn.db.posts.find_one({"_id": post_id_obj}, {"title": 1, "created_on": 1, "_id": 0})
        
        post_title = post.get("title")
        post_date = post.get("created_on")

        post_details = []
        post_details.append(post_title)
        post_details.append(post_date)
        
        post_dict.update({post_id: post_details})

        return post_dict