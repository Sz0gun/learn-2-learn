from fastapi import FastAPI, Request
from pydantic import BaseModel
import redis

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0)

class Item(BaseModel):
    key: str
    value: str

@app.post("/set_value")
async def set_value(request: Request, item: Item):
    # Logowanie danych z JSON
    json_data = await request.json()
    print(json_data)
    r.set(item.key, item.value)
    return {"message": f"Value set for key: {item.key}"}
