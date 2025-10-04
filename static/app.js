// app.js

// DOM(Document Object Model)이 완전히 로드된 후에 스크립트를 실행합니다.
// 이렇게 하면 HTML 요소들이 모두 준비된 상태에서 JS 코드가 실행되어 오류를 방지합니다.
document.addEventListener('DOMContentLoaded', () => {

    // HTML에서 필요한 요소들을 가져옵니다.
    const memoForm = document.getElementById('memo-form');
    const memoInput = document.getElementById('memo-input');
    const memoList = document.getElementById('memo-list');

    // [READ] 서버에서 모든 메모를 가져와 화면에 표시하는 함수
    const fetchMemos = async () => {
        try {
            // /api/memos 경로로 GET 요청을 보냅니다.
            const response = await fetch('/api/memos');
            if (!response.ok) {
                throw new Error('메모를 불러오는 데 실패했습니다.');
            }
            // 응답받은 JSON 데이터를 JavaScript 객체 배열로 변환합니다.
            const memos = await response.json();

            // 기존 메모 목록을 비웁니다.
            memoList.innerHTML = '';

            // 각 메모에 대해 HTML 요소를 생성하고 목록에 추가합니다.
            memos.forEach(memo => {
                const memoItem = document.createElement('div');
                memoItem.classList.add('memo-item');
                memoItem.textContent = memo.content;
                memoList.appendChild(memoItem);
            });
        } catch (error) {
            console.error(error);
            memoList.innerHTML = '<div class="memo-item">메모를 불러올 수 없습니다.</div>';
        }
    };

    // [CREATE] 새 메모를 서버에 추가하는 함수
    const addMemo = async (content) => {
        try {
            // /api/memos 경로로 POST 요청을 보냅니다.
            const response = await fetch('/api/memos', {
                method: 'POST',
                // 보내는 데이터의 타입을 JSON으로 명시합니다.
                headers: {
                    'Content-Type': 'application/json',
                },
                // JavaScript 객체를 JSON 문자열로 변환하여 요청 본문에 담습니다.
                body: JSON.stringify({ content: content }),
            });

            if (!response.ok) {
                throw new Error('메모 추가에 실패했습니다.');
            }

            // 메모 추가에 성공하면 입력창을 비우고, 전체 메모 목록을 다시 불러옵니다.
            memoInput.value = '';
            fetchMemos();

        } catch (error) {
            console.error(error);
            alert('메모를 추가할 수 없습니다.');
        }
    };

    // 폼(form)이 제출(submit)되었을 때의 이벤트를 처리합니다.
    memoForm.addEventListener('submit', (event) => {
        // 폼 제출 시 페이지가 새로고침되는 기본 동작을 막습니다.
        event.preventDefault();

        // 입력창의 텍스트를 가져옵니다. trim()으로 양쪽 공백을 제거합니다.
        const newMemoContent = memoInput.value.trim();

        // 내용이 비어있지 않으면 addMemo 함수를 호출합니다.
        if (newMemoContent) {
            addMemo(newMemoContent);
        }
    });

    // 페이지가 처음 로드될 때 서버에서 메모 목록을 가져옵니다.
    fetchMemos();
});
