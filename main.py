# main.py

# 필요한 라이브러리들을 가져옵니다.
import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- 데이터베이스 모델 정의 ---
# SQLModel을 사용하여 데이터베이스 테이블과 API 데이터 모델을 한 번에 정의합니다.
class Memo(SQLModel, table=True):
    # id: 기본 키(Primary Key)이며, 자동으로 값이 증가하는 정수입니다.
    # Optional[int]는 새 메모를 생성할 때는 id가 없어도 되기 때문입니다.
    id: int | None = Field(default=None, primary_key=True)
    # content: 메모의 내용을 담는 문자열 필드입니다.
    content: str

# --- 데이터베이스 설정 ---
# 로컬 개발 환경에서는 간단한 SQLite 데이터베이스 파일을 사용합니다.
# Render.com에 배포될 때는 Render가 제공하는 DATABASE_URL 환경 변수를 사용하게 됩니다.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# 데이터베이스 엔진을 생성합니다.
# echo=True는 실행되는 SQL 쿼리를 콘솔에 출력하여 디버깅에 도움을 줍니다.
engine = create_engine(DATABASE_URL, echo=True)

# FastAPI 앱이 시작될 때 데이터베이스 테이블을 생성하는 함수입니다.
def create_db_and_tables():
    # Memo 모델에 정의된 모든 테이블을 데이터베이스에 생성합니다.
    SQLModel.metadata.create_all(engine)

# --- FastAPI 앱 설정 ---
# FastAPI 애플리케이션 인스턴스를 생성합니다.
app = FastAPI()

# FastAPI 앱이 시작될 때 create_db_and_tables 함수를 실행하도록 설정합니다.
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# --- 데이터베이스 세션 관리 ---
# API 요청이 있을 때마다 데이터베이스 세션을 생성하고, 요청 처리가 끝나면 세션을 닫는
# 의존성 함수(Dependency)입니다. 이를 통해 API 각 요청은 독립적인 DB 트랜잭션을 갖게 됩니다.
def get_session():
    with Session(engine) as session:
        yield session

# --- API 엔드포인트 정의 ---

# [CREATE] 새 메모를 생성하는 API
# POST 요청을 /api/memos 경로로 받습니다.
# response_model=Memo는 이 API의 응답 형식이 Memo 모델과 같다는 것을 명시합니다.
@app.post("/api/memos", response_model=Memo)
def create_memo(memo: Memo, session: Session = Depends(get_session)):
    # 클라이언트로부터 받은 memo 객체를 데이터베이스 세션에 추가합니다.
    session.add(memo)
    # 변경사항을 데이터베이스에 커밋(저장)합니다.
    session.commit()
    # 저장된 객체를 다시 로드하여 최신 상태(예: 자동 생성된 id 포함)로 만듭니다.
    session.refresh(memo)
    # 저장된 메모 객체를 클라이언트에 반환합니다.
    return memo

# [READ] 모든 메모를 조회하는 API
# GET 요청을 /api/memos 경로로 받습니다.
# response_model=List[Memo]는 Memo 객체의 리스트 형태로 응답한다는 것을 명시합니다.
@app.get("/api/memos", response_model=list[Memo])
def read_memos(session: Session = Depends(get_session)):
    # 데이터베이스에서 모든 Memo 객체를 조회합니다.
    memos = session.exec(select(Memo)).all()
    # 조회된 메모 목록을 반환합니다.
    return memos

# --- 정적 파일 서빙 설정 ---
# API 엔드포인트들이 모두 정의된 후에 와야 합니다.
# "/" 경로로 들어오는 요청을 "static" 디렉토리의 파일로 처리합니다.
# html=True는 사용자가 "/"(루트) 경로로 접속했을 때 "static/index.html"을 보여주도록 합니다.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
