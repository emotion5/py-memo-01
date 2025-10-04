// app.js

document.addEventListener('DOMContentLoaded', () => {

    const memoForm = document.getElementById('memo-form');
    const memoInput = document.getElementById('memo-input');
    const memoList = document.getElementById('memo-list');

    // [DELETE] 서버에서 특정 메모를 삭제하는 함수
    const deleteMemo = async (memoId) => {
        try {
            const response = await fetch(`/api/memos/${memoId}`, {
                method: 'DELETE',
            });

            if (!response.ok) {
                throw new Error('메모 삭제에 실패했습니다.');
            }

            // 메모 삭제 성공 시, 전체 메모 목록을 다시 불러옵니다.
            fetchMemos();

        } catch (error) {
            console.error(error);
            alert('메모를 삭제할 수 없습니다.');
        }
    };

    // [READ] 서버에서 모든 메모를 가져와 화면에 표시하는 함수
    const fetchMemos = async () => {
        try {
            const response = await fetch('/api/memos');
            if (!response.ok) {
                throw new Error('메모를 불러오는 데 실패했습니다.');
            }
            const memos = await response.json();

            memoList.innerHTML = '';

            memos.forEach(memo => {
                const memoItem = document.createElement('div');
                memoItem.classList.add('memo-item');

                const memoContent = document.createElement('span');
                memoContent.textContent = memo.content;

                const deleteButton = document.createElement('button');
                deleteButton.classList.add('delete-btn');
                deleteButton.textContent = '삭제';
                deleteButton.addEventListener('click', () => {
                    deleteMemo(memo.id);
                });

                memoItem.appendChild(memoContent);
                memoItem.appendChild(deleteButton);
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
            const response = await fetch('/api/memos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ content: content }),
            });

            if (!response.ok) {
                throw new Error('메모 추가에 실패했습니다.');
            }

            memoInput.value = '';
            fetchMemos();

        } catch (error) {
            console.error(error);
            alert('메모를 추가할 수 없습니다.');
        }
    };

    memoForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const newMemoContent = memoInput.value.trim();
        if (newMemoContent) {
            addMemo(newMemoContent);
        }
    });

    fetchMemos();
});