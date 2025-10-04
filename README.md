# FastAPI & SQLModel 서버 구성 계획서

본 문서는 FastAPI와 SQLModel을 사용하여 프론트엔드에 데이터 API를 제공하는 백엔드 서버의 구성 계획을 정의합니다. 서버와 데이터베이스는 Render.com 클라우드 서비스를 사용하여 배포 및 운영됩니다.

## 1. 핵심 목표

- 프론트엔드 애플리케이션에서 데이터를 기록하고 조회할 수 있는 안정적인 API 서버를 구축합니다.
- Python의 타입 힌트를 적극적으로 활용하여 데이터 유효성을 검증하고 코드 안정성을 높입니다.
- SQL 쿼리문 없이 Python 코드로 데이터베이스 작업을 처리(CRUD)합니다.
- Render.com의 관리형 서비스를 통해 인프라 관리 부담을 최소화하고 빠르게 배포합니다.

## 2. 기술 스택 및 역할

| 기술            | 역할                                                                                             |
| --------------- | ------------------------------------------------------------------------------------------------ |
| **FastAPI**     | API 서버 구축, URL 라우팅, 데이터 검증, 자동 API 문서 생성                                       |
| **SQLModel**    | 데이터베이스 테이블 구조 모델링 및 ORM(Object-Relational Mapping) 기능 제공                      |
| **Uvicorn**     | FastAPI 애플리케이션을 실행하는 고성능 ASGI(Asynchronous Server Gateway Interface) 서버            |
| **PostgreSQL**  | Render.com에서 제공하는 관리형 데이터베이스 서비스                                               |
| **psycopg2-binary** | SQLModel(SQLAlchemy)이 PostgreSQL 데이터베이스와 통신할 수 있도록 하는 Python 드라이버         |
| **Render.com**  | FastAPI 웹 서비스 및 PostgreSQL 데이터베이스 호스팅                                              |

## 3. 가상 환경 및 의존성 관리 (venv + uv)

프로젝트의 의존성을 격리하고 빠르게 관리하기 위해 Python 표준 가상 환경(`venv`)과 고성능 패키지 설치 도구 `uv`를 사용합니다.

1.  **uv 설치 (최초 1회):**
    ```bash
    pip install uv
    ```

2.  **가상 환경 생성 및 활성화:**
    ```bash
    # 가상 환경 생성 (.venv 폴더 생성)
    uv venv

    # 가상 환경 활성화 (macOS/Linux)
    source .venv/bin/activate

    # 가상 환경 활성화 (Windows)
    .venv\Scripts\activate
    ```

3.  **의존성 관리 파일 (`requirements.txt`):**
    Render.com 배포 호환성을 위해 `requirements.txt` 파일을 계속 사용합니다. 내용은 동일합니다.
    ```
    fastapi
    sqlmodel
    uvicorn
    psycopg2-binary
    ```

4.  **의존성 설치:**
    활성화된 가상 환경에서 `uv`를 사용하여 `requirements.txt` 파일의 패키지들을 설치합니다.
    ```bash
    uv pip install -r requirements.txt
    ```

## 4. 로컬 개발 서버 실행

가상 환경이 활성화된 상태에서 아래 명령어를 실행하여 개발 서버를 시작합니다.

```bash
uvicorn main:app --reload
```
- `--reload` 옵션은 코드 변경 시 서버를 자동으로 재시작하여 개발 편의성을 높여줍니다.

## 5. 프론트엔드 구성 계획 (정적 페이지)

초기 단계에서는 별도의 프론트엔드 프로젝트를 분리하지 않고, FastAPI 백엔드에 정적 파일(HTML, CSS, JS)을 포함하여 한 번에 서빙합니다. 이를 통해 개발 환경을 단순화하고 빠른 프로토타이핑을 진행합니다. 프로젝트 규모가 커지면 향후 분리를 고려합니다.

### 5.1. 파일 구조

`static` 폴더를 생성하여 프론트엔드 관련 파일을 관리합니다.

```
/
├── static/
│   ├── index.html  # 메인 페이지
│   ├── style.css   # 스타일시트
│   └── app.js      # 클라이언트 사이드 로직
├── main.py         # FastAPI 앱
└── requirements.txt
```

### 5.2. 기능 명세

- **입력**: 한 줄 메모를 입력할 수 있는 텍스트 입력창
- **저장**: 메모를 서버에 저장하는 '추가' 버튼
- **조회**: 서버에서 불러온 메모 목록을 보여주는 영역
- **동작**: 페이지 로드 시 기존 메모 목록을 API로 불러오고, '추가' 버튼 클릭 시 새 메모를 API로 저장한 후 목록을 갱신합니다.

### 5.3. 디자인 컨셉

- **색상**: 완전한 흑백(Monotone)을 기반으로, 회색 계열(Grayscale)을 사용하여 깊이감을 조절합니다. (예: 배경-어두운 회색, 텍스트-흰색, 버튼-밝은 회색)
- **형태**: 모든 UI 요소(버튼, 입력창 등)는 `border-radius: 0;`을 적용하여 둥근 모서리 없이 각진 형태로 디자인합니다.
- **레이아웃**: 복잡한 요소를 배제하고, 핵심 기능(입력, 추가, 목록)을 수직으로 단순하게 배치하여 가독성을 높입니다.

## 6. FastAPI 정적 파일 서빙 설정

FastAPI가 `static` 폴더 안의 `index.html`과 다른 파일들을 서빙할 수 있도록 `main.py`에 `StaticFiles`를 마운트하는 설정이 필요합니다.

## 7. Render.com 배포 계획

### 7.1. PostgreSQL 데이터베이스 생성

1.  Render 대시보드에서 **[New]** > **[PostgreSQL]**을 선택하여 새 데이터베이스를 생성합니다.
2.  생성된 데이터베이스의 **Connect** 정보에서 **`Internal Database URL`**을 복사합니다.

### 7.2. FastAPI 웹 서비스 생성

1.  Render 대시보드에서 **[New]** > **[Web Service]**를 선택하고 Git 리포지토리를 연결합니다.
2.  아래와 같이 빌드 및 실행 설정을 구성합니다.
    -   **Build Command**: `uv pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 7.3. 데이터베이스 연결 설정 (환경 변수)

1.  생성한 Web Service의 **[Environment]** 탭에서 새 환경 변수를 추가합니다.
    -   **Key**: `DATABASE_URL`
    -   **Value**: `7.1` 단계에서 복사한 **`Internal Database URL`**을 붙여넣습니다.

## 8. FastAPI 애플리케이션 코드 예시 (정적 파일 포함)

`main.py`는 API 로직과 더불어 정적 파일을 서빙하는 역할도 함께 수행합니다.

**`main.py` (예시):**
```python
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import create_engine

# --- 데이터베이스 설정 ---
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

# --- FastAPI 앱 생성 ---
app = FastAPI()

# --- API 엔드포인트 (여기에 CRUD 구현) ---
@app.get("/api/hello")
def read_root():
    return {"message": "API가 정상적으로 실행 중입니다."}

# --- 정적 파일 서빙 ---
# API 라우터들이 모두 등록된 후에 마지막에 추가해야 합니다.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
```
