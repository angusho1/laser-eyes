let currInputFile;

function openFileExplorer() {
    const input = document.getElementById('fileInput');
    input.click();
    input.onchange = onFileSelect;
}

function onFileSelect(e) {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        currInputFile = file;
        const formData = new FormData();
        formData.append('image', file);
        formData.append('laserScale', getLaserScale());
        uploadImage(formData);
        
        const fileText = document.getElementById('selected-file-text');
        fileText.textContent = `Selected File: ${file.name}`;
    }
}

function uploadImage(formData) {
    setLoadingBtn();
    const http = new XMLHttpRequest();
    http.onreadystatechange = function() {
        if (http.readyState == XMLHttpRequest.DONE) {
            const img = document.getElementById('output-canvas');
            img.src = 'data:image/jpeg;base64,' + http.responseText;
            resetLoadingBtn();
            
            const downloadBtn = document.getElementById('download-btn');
            if (downloadBtn.classList.contains('btn-disabled')) {
                downloadBtn.classList.remove('btn-disabled');
            }

            const updateBtn = document.getElementById('update-btn');
            if (updateBtn.classList.contains('btn-disabled')) {
                updateBtn.classList.remove('btn-disabled');
            }
        }
    }

    const url = '/process';

    http.open('POST', url);
    http.send(formData);
}

function setLoadingBtn() {
    const button = document.getElementById('upload-btn');
    if (!button.classList.contains('loading')) {
        button.classList.add('loading');
        const svg = button.querySelector('svg');
        if (svg) {
            svg.style.display = 'none';
        }
    }
}

function resetLoadingBtn() {
    const button = document.getElementById('upload-btn');
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
    const formData = new FormData();
    formData.append('image', currInputFile)
    formData.append('laserScale', getLaserScale());
    uploadImage(formData);
}

function getLaserScale() {
    const input = document.getElementById('laserScaleInput');
    return input.value / 100;
}