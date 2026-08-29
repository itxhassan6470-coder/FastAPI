from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
async def home():
    return FileResponse("index.html")

@app.get("/about")
async def about():
    return FileResponse("about.html")