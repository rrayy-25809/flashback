var sliced = location.href.slice(0, -5);
const post_image = sliced+'post_image'; // 요청을 보낼 URL
const post_video = sliced+'post_video'; // 요청을 보낼 URL

// 이미지와 스토리보드 HTML 템플릿을 반환하는 함수
function output_image(img) {
    const output_image = `
    <img class="output-image rounded-4" src="${img}" />
    <div class="storyboard">
        <h5>Explain Storyboard</h5>
        <textarea id="storyboard" placeholder="Describe the storyboard here"></textarea>
        <div class="buttons">
            <button class="button-vr" onclick="window.open('/viewer')"></button>
            <button class="button-next" onclick="next()"></button>
        </div>
    </div>
    <div id="loading-overlay">
        <div class="spinner-border text-secondary" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>`;
    return output_image;
}

// 로딩 오버레이를 화면에 표시하는 함수
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

// 로딩 오버레이를 화면에서 숨기는 함수
function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// 이미지와 텍스트 입력을 받아 처리한 후, 결과를 화면에 표시하는 함수
function generate() {
    const image_input = document.getElementById("image-input");
    const file = image_input.files[0]; // 선택된 파일 가져오기
    const prompt_input = document.getElementById("prompt-input").value;  // 텍스트 입력 값 가져오기
    const output = document.getElementById("right");
    const checkbox = document.getElementById('flexSwitchCheckDefault');
    //console.log(checkbox.checked)
    if (file) {
        showLoading();  // 로딩 오버레이 표시
        const formData = new FormData();
        formData.append('image', file); // 파일을 FormData에 추가
        formData.append('prompt',prompt_input)
        formData.append('is_remix',checkbox.checked)
        
        // fetch 요청
        fetch(post_image, {
            method: 'POST',
            body: formData, // FormData 객체를 body에 전달
        })
        .then(response => {
            if (!response.ok) {
                alert("요청을 보내는 중 문제가 발생했습니다. 이미지와 프롬포트가 적절한지 확인하세요.");
                hideLoading();
                throw new Error(response.statusText);
            }
            return response.text(); // 응답을 텍스트로 변환
        })
        .then(data => {
            console.log('성공:', data);
            hideLoading();  // 로딩 오버레이 숨기기
            output.innerHTML = output_image(`/static/${data}.png`);  // 이미지와 스토리보드 출력
        })
        .catch(error => {
            console.log('오류:', error);
        });
    } else {
        alert('파일을 선택하세요.');
    }
}

// 다음 단계를 처리하는 함수
function next() {
    const storyboard = document.getElementById("storyboard").value;
    showLoading();  // 로딩 오버레이 표시
    const formData = new FormData();
    formData.append("storyboard",storyboard)
    fetch(post_video, {
        method: 'POST',
        body: formData, // FormData 객체를 body에 전달
    })
    .then(response => {
        if (!response.ok) {
            alert("요청을 보내는 중 문제가 발생했습니다. 다시 시도해 주세요.");
            hideLoading();
            throw new Error(response.statusText);
        }
        return response.text(); // 응답을 텍스트로 변환
    })
    .then(data => {
        console.log('성공:', data);
        hideLoading();  // 로딩 오버레이 숨기기
        window.open(`/viewer_video/${data}`)
    })
    .catch(error => {
        console.log('오류:', error);
    });
}