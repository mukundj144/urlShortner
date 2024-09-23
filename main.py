from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse, FileResponse
from database import URLs  # Assuming your database module is named 'database.py'
from pymongo import MongoClient
from qrcode import qr_code

# MongoDB connection setup
connection_string = "mongodb://localhost:27017"
mongo_db = MongoClient(connection_string)
database = mongo_db.UrlShortner
collection = database.URLs

# URL and QR code objects
url_obj = URLs(collection)
qr_obj = qr_code()  # Instantiate qr_code object

# Define base URL (for example, your local host or domain name)
base_url = "https://mukund-urlshortner.onrender.com"

# Pydantic model for the incoming URL data
class AddURL(BaseModel):
    special_key: str
    url: str

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def hello():
    return "HELLO FASTAPI WORLD"

@app.get("/{specialKey}")
async def new(specialKey: str):
    url = url_obj.fetch_url(specialKey)
    if url:
        return RedirectResponse(url, status_code=302)
    else:
        return {"error": "URL not found"}

@app.post("/addURL")
async def add_url(json: AddURL):
    insert = url_obj.insert_url(json.special_key, json.url)
    if insert:
        return {"Shortened URL": base_url + json.special_key}
    return {"error": "URL with this special key already exists"}

@app.get("/count/{specialkey}")
async def count_clicks(specialkey: str):
    count = url_obj.count(specialkey)
    return {"Click count": count}

@app.get("/qrcode/{specialkey}")
async def make_qr(specialkey: str):
    qr_obj.make_qr(base_url + specialkey, specialkey)
    return FileResponse(f"{specialkey}.png")
