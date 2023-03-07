from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/redirect")
async def redirect():
    return {"message": "Redirected"}