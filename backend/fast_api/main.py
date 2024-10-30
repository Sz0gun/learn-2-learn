from fast_api import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Wellcome to AI Kitchen!"}

@app.get("/status")
def status():
    return {"status": "Running"}