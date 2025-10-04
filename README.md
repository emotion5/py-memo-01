# FastAPI-Firestore 메모 앱

A simple memo application built with FastAPI and Vanilla JS, using Google Firestore as the database, and deployed on Vercel.

## ✨ 주요 기능

- **메모 작성**: 새로운 메모를 작성하고 저장합니다.
- **메모 조회**: 저장된 모든 메모를 최신순으로 불러옵니다.
- **메모 삭제**: 각 메모를 개별적으로 삭제합니다.
- **영구 저장**: 데이터는 Google Firestore에 안전하게 저장됩니다.

## 🛠️ 기술 스택

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla JavaScript, HTML, CSS
- **Database**: Google Firestore
- **Deployment**: Vercel

## 🚀 배포 및 설정 방법

이 프로젝트는 Vercel을 통해 간단하게 배포할 수 있습니다.

### 1. Firebase 프로젝트 설정

1.  **Firebase 프로젝트 생성**: [Firebase Console](https://console.firebase.google.com/)에서 새 프로젝트를 생성합니다.
2.  **Firestore 활성화**: 생성한 프로젝트에서 **Firestore Database**를 생성하고 `테스트 모드` 또는 `프로덕션 모드`로 시작합니다.
3.  **서비스 계정 키 생성**:
    - 프로젝트 설정 > `서비스 계정` 탭으로 이동합니다.
    - `새 비공개 키 생성` 버튼을 눌러 `.json` 형식의 키 파일을 다운로드합니다. 이 파일은 안전하게 보관해야 합니다.

### 2. Vercel 배포

1.  **저장소 Fork & Clone**: 이 GitHub 저장소를 자신의 계정으로 Fork한 후, 로컬 컴퓨터에 Clone합니다.
2.  **Vercel 프로젝트 생성**: [Vercel 대시보드](https://vercel.com/dashboard)에서 `Add New...` > `Project`를 선택하고, Fork한 Git 저장소를 Import합니다.
3.  **환경 변수 설정**:
    - Vercel 프로젝트의 `Settings` > `Environment Variables` 메뉴로 이동합니다.
    - 아래와 같이 환경 변수를 추가합니다.
      - **Name**: `FIREBASE_SERVICE_ACCOUNT_KEY`
      - **Value**: 1단계에서 다운로드한 `.json` 파일의 **내용 전체**를 복사하여 붙여넣습니다.
4.  **배포**: `Deploy` 버튼을 클릭하여 배포를 시작합니다.

### 3. Firestore 설정 (배포 후)

- **보안 규칙**: (프로덕션 모드로 시작한 경우) Firebase Console의 `Firestore Database` > `규칙` 탭에서 아래와 같이 모든 읽기/쓰기를 허용하는 규칙으로 변경해야 앱이 정상 작동합니다.
  ```
  rules_version = '2';
  service cloud.firestore {
    match /databases/{database}/documents {
      match /{document=**} {
        allow read, write: if true;
      }
    }
  }
  ```
- **인덱스 생성**: 앱 배포 후, 메모를 정렬하는 과정에서 Firestore 인덱스가 필요하다는 에러가 Vercel 로그에 나타날 수 있습니다. 이 경우, 로그에 포함된 링크를 클릭하여 필요한 인덱스를 간단하게 생성할 수 있습니다.