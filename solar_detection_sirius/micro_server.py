from fastapi import FastAPI

app = FastAPI()

@app.get("/datetime")
def get_data():
    return {"datetime": "datetime"}

# Build
# pip install fastapi uvicorn
# uvicorn micro_server:app --reload