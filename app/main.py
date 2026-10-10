from fastapi import FastAPI

app = FastAPI(title="Loan Affordability Assistant")


@app.get("/health")
def health_check():
    return {"status": "ok"}
