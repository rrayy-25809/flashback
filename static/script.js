const checkbox = document.getElementById('flexSwitchCheckDefault');

// 이미지와 스토리보드 HTML 템플릿을 반환하는 함수
function output_image(img) {
    const output_image = `
    <img class="output-image rounded-4" src="${img}" />
    <div class="storyboard">
        <h5>Explain Storyboard</h5>
        <textarea placeholder="Describe the storyboard here"></textarea>
        <div class="buttons">
            <button class="button-vr" onclick="window.open('viewer.html')"></button>
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
    const image_input = document.getElementById("image-input");  // 입력 이미지의 태그 이름 가져오기
    const prompt_input = document.getElementById("prompt-input").value;  // 텍스트 입력 값 가져오기
    const output = document.getElementById("right");

    showLoading();  // 로딩 오버레이 표시

    setTimeout(() => {
        hideLoading();  // 로딩 오버레이 숨기기
        alert(`${checkbox.checked} ${image_input.tagName} ${prompt_input}`);  // 체크박스, 이미지 입력, 텍스트 입력 값 확인
        output.innerHTML = output_image("/img/test_image.png");  // 이미지와 스토리보드 출력
    }, 3000); // 3초 뒤에 로딩 화면 숨김 (예시)
}

// 다음 단계를 처리하는 함수
function next() {
    showLoading();  // 로딩 오버레이 표시

    // 필요한 처리 로직 추가
    setTimeout(() => {
        hideLoading();  // 로딩 오버레이 숨기기
    }, 3000); // 3초 뒤에 로딩 화면 숨김 (예시)
}