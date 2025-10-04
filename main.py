# main.py (수정 예시)
import os
import json
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import firebase_admin
from firebase_admin import credentials, firestore

# --- Firebase 설정 ---
# Vercel 환경 변수에서 서비스 계정 키를 가져옵니다.
service_account_key_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
if service_account_key_json:
    creds_dict = json.loads(service_account_key_json)
    cred = credentials.Certificate(creds_dict)
    firebase_admin.initialize_app(cred)
else:
    # 로컬 개발용 (기본 설정)
    # 이 경우, GOOGLE_APPLICATION_CREDENTIALS 환경변수가 설정되어 있어야 합니다.
    print("WARNING: FIREBASE_SERVICE_ACCOUNT_KEY not found. Using default credentials.")
    firebase_admin.initialize_app()

db = firestore.client()

class Memo(BaseModel):
    id: str  # Firestore는 ID로 문자열을 사용합니다.
    content: str

class MemoCreate(BaseModel):
    content: str

app = FastAPI()

@app.post("/api/memos", response_model=Memo)
def create_memo(memo: MemoCreate):
    # Firestore 'memos' 컬렉션에 새 문서를 추가합니다.
    doc_ref = db.collection('memos').add({'content': memo.content})
    new_memo = Memo(id=doc_ref[1].id, content=memo.content)
    return new_memo

@app.get("/api/memos", response_model=List[Memo])
def read_memos():
    memos = []
    # 'memos' 컬렉션의 모든 문서를 시간순으로 정렬하여 가져옵니다.
    for doc in db.collection('memos').order_by("content").stream():
        memo_data = doc.to_dict()
        if memo_data:
            memos.append(Memo(id=doc.id, **memo_data))
    return memos

app.mount("/", StaticFiles(directory="static", html=True), name="static")
