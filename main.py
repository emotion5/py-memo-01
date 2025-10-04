# main.py
import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import firebase_admin
from firebase_admin import credentials, firestore

# --- Firebase 설정 ---
service_account_key_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
if service_account_key_json:
    creds_dict = json.loads(service_account_key_json)
    cred = credentials.Certificate(creds_dict)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
else:
    print("WARNING: FIREBASE_SERVICE_ACCOUNT_KEY not found. Using default credentials.")
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

db = firestore.client()

class Memo(BaseModel):
    id: str
    content: str

class MemoCreate(BaseModel):
    content: str

app = FastAPI()

@app.post("/api/memos", response_model=Memo)
def create_memo(memo: MemoCreate):
    # Firestore에 content와 함께 서버 시간을 timestamp로 저장합니다.
    doc_ref = db.collection('memos').add({
        'content': memo.content,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    new_memo = Memo(id=doc_ref[1].id, content=memo.content)
    return new_memo

@app.get("/api/memos", response_model=List[Memo])
def read_memos():
    memos = []
    # timestamp를 기준으로 내림차순(최신순)으로 정렬하여 문서를 가져옵니다.
    for doc in db.collection('memos').order_by("timestamp", direction="DESCENDING").stream():
        memo_data = doc.to_dict()
        if memo_data:
            memos.append(Memo(id=doc.id, **memo_data))
    return memos

@app.delete("/api/memos/{memo_id}", status_code=204)
def delete_memo(memo_id: str):
    # Firestore에서 해당 ID의 문서를 삭제합니다.
    doc_ref = db.collection('memos').document(memo_id)
    if not doc_ref.get().exists:
        raise HTTPException(status_code=404, detail="Memo not found")
    doc_ref.delete()
    return

app.mount("/", StaticFiles(directory="static", html=True), name="static")