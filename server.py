from fastapi import FastAPI

app = FastAPI()

@app.get("/") # line 48 in fastapi/applications.py
async def root():
    return {"message": "Hello World"}