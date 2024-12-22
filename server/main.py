from fastapi import FastAPI

app = FastAPI()

@app.get("/datetime")
def get_data():
    return {"datetime": "datetime"}
