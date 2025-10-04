# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

# --- In-memory data storage ---
# A simple list to store memos in memory.
# This will be reset every time the application restarts.
memos_db = []
memo_id_counter = 1

# --- Pydantic Model ---
# Defines the structure of a memo for request and response validation.
class Memo(BaseModel):
    id: int
    content: str

class MemoCreate(BaseModel):
    content: str

# --- FastAPI App ---
app = FastAPI()

# --- API Endpoints ---

@app.post("/api/memos", response_model=Memo)
def create_memo(memo_in: MemoCreate):
    global memo_id_counter
    new_memo = Memo(id=memo_id_counter, content=memo_in.content)
    memos_db.append(new_memo)
    memo_id_counter += 1
    return new_memo

@app.get("/api/memos", response_model=List[Memo])
def read_memos():
    return memos_db

# --- Static Files ---
# This must come after all API endpoints.
# It serves the frontend files from the "static" directory.
app.mount("/", StaticFiles(directory="static", html=True), name="static")