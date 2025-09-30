from fastapi import FastAPI

app = FastAPI()

@app.options("/health")
def health_check():
    return {"status": "ok"}
