class URLs:
    def __init__(self, obj_mongoDb_collection):
        self.db = obj_mongoDb_collection   
    
    def insert_url(self, special_key, url):
        if self.db.count_documents({"special_key": special_key}) > 0:
            return False
        else:
            doc = {
                "special_key": special_key,
                "url": url,
                "clicks": clicks
            } 
            self.db.insert_one(doc)
            return True
    
    def fetch_url(self, special_key):
        try:
            data = self.db.find_one({"special_key": special_key})
            self.db.update_one({"special_key":special_key},{"$inc":{"clicks":1}})
            if data:
                return data['url']  
            else:
                return "https://yahoo.com"
        except:
            return "https://google.com"
    
    def count(self,special_key):
        try:
            data = self.db.find_one({"special_key":special_key})
            return data["clicks"]
        except:
            return 0
