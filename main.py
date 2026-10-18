from fastapi import FastAPI

app = FastAPI(title= "Job Portal API")


@app.get("/")
def home():
    return {
        "message" : "Job Portal API is running"
    }