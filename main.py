from fastapi import FastAPI
app = FastAPI()
@app.get("/hello")
def start():
    return {"message": "swagat hai gandu"}

@app.get('/bye/{name}')
def end(name:str):
    return f"bye {name}"