let currInputFile;
let currImageDetectionResults;

function openFileExplorer() {
    const input = document.getElementById('fileInput');
    input.click();
    input.onchange = onFileSelect;
}

function onFileSelect(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        currInputFile = file;

        setLoadingBtn('upload-btn');
        getFaceDetectionResults(file)
            .then(res => {
                currImageDetectionResults = res;
                return getAppliedImage(file, res, getLaserScale());
            })
            .then(imageData => {
                setImage(imageData);
                enableUtilButtons();
            })
            .finally(() => resetLoadingBtn('upload-btn'));
        
        const fileText = document.getElementById('selected-file-text');
        fileText.textContent = `Selected File: ${file.name}`;
    }
}

function getFaceDetectionResults(imageFile) {
    return new Promise((res, rej) => {
        const formData = new FormData();
        formData.append('image', imageFile);
        const http = new XMLHttpRequest();

        http.onreadystatechange = () => {
            if (http.readyState == XMLHttpRequest.DONE) {
                if (http.status === 200) {
                    res(http.responseText);
                } else {
                    rej(http.response);
                }
            }
        }
        
        http.open('POST', '/detect');
        http.send(formData);
    });
}

function getAppliedImage(imageFile, detectionResults, laserScale) {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('faces', detectionResults);
    formData.append('laserScale', laserScale);
    const http = new XMLHttpRequest();

    return new Promise((res, rej) => {
        http.onreadystatechange = () => {
            if (http.readyState == XMLHttpRequest.DONE) {
                if (http.status === 200) {
                    const imageData = 'data:image/jpeg;base64,' + http.responseText;
                    res(imageData);
                } else {
                    rej(http.response);
                }
            }
        }
        
        http.open('POST', '/apply');
        http.send(formData);
    });
}

function setLoadingBtn(className) {
    const button = document.getElementById(className);
    if (!button.classList.contains('loading')) {
        button.classList.add('loading');
        const svg = button.querySelector('svg');
        if (svg) {
            svg.style.display = 'none';
        }
    }
}

function resetLoadingBtn(className) {
    const button = document.getElementById(className);
    if (button.classList.contains('loading')) {
        button.classList.remove('loading');
        const svg = button.querySelector('svg');
        if (svg) {
            svg.style.display = '';
        }
    }
}

function downloadImage() {
    // Ref: https://ourcodeworld.com/articles/read/189/how-to-create-a-file-and-generate-a-download-with-javascript-in-the-browser-without-a-server
    const img = document.getElementById('output-canvas');
    const filename = `laser_${currInputFile.name}`;
    
    const element = document.createElement('a');
    element.setAttribute('href', img.src);
    element.setAttribute('download', filename);
    
    element.style.display = 'none';
    document.body.appendChild(element);
    
    element.click();
    
    document.body.removeChild(element);
}

function updateImage() {
    setLoadingBtn('update-btn');
    getAppliedImage(currInputFile, currImageDetectionResults, getLaserScale())
        .then(imageData => {
            setImage(imageData);
        })
        .finally(() => resetLoadingBtn('update-btn'));
}

function getLaserScale() {
    const input = document.getElementById('laserScaleInput');
    return input.value / 100;
}

function enableUtilButtons() {
    const downloadBtn = document.getElementById('download-btn');
    if (downloadBtn.classList.contains('btn-disabled')) {
        downloadBtn.classList.remove('btn-disabled');
    }
    
    const updateBtn = document.getElementById('update-btn');
    if (updateBtn.classList.contains('btn-disabled')) {
        updateBtn.classList.remove('btn-disabled');
    }
}

function setImage(imageData) {
    const img = document.getElementById('output-canvas');
    img.src = imageData;
}