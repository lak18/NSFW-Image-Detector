document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file-input');
    const detectBtn = document.getElementById('detect-btn');
    const resultSection = document.getElementById('result-section');
    const resultContent = document.getElementById('result-content');
    
    let selectedFile = null;

    fileInput.addEventListener('change', function(e) {
        selectedFile = e.target.files[0];
        if (selectedFile) {
            detectBtn.disabled = false;
            // Show the file name
            resultSection.classList.remove('hidden');
            resultContent.innerHTML = `
                <div style="text-align: center;">
                    <p>Selected file: ${selectedFile.name}</p>
                </div>
            `;
        } else {
            detectBtn.disabled = true;
        }
    });

    detectBtn.addEventListener('click', function() {
        if (!selectedFile) {
            return;
        }

        // Show loading state
        resultSection.classList.remove('hidden');
        resultContent.innerHTML = `
            <div style="text-align: center;">
                <p>Selected file: ${selectedFile.name}</p>
                <p>Analyzing image...</p>
                <div class="progress-container">
                    <div class="progress-bar" id="progress-bar"></div>
                </div>
            </div>
        `;

        // Animate progress bar
        const progressBar = document.getElementById('progress-bar');
        let width = 0;
        const interval = setInterval(() => {
            if (width >= 90) {
                clearInterval(interval);
            } else {
                width += 5;
                progressBar.style.width = width + '%';
            }
        }, 150);

        const formData = new FormData();
        formData.append('file', selectedFile);

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(interval);
            progressBar.style.width = '100%';
            
            if (data.error) {
                resultContent.innerHTML = `
                    <p>Selected file: ${selectedFile.name}</p>
                    <p style="color: red; text-align: center;">Error: ${data.error}</p>
                `;
                return;
            }

            // Process the data
            setTimeout(() => {
                displayResults(data);
            }, 500);
        })
        .catch(error => {
            clearInterval(interval);
            resultContent.innerHTML = `
                <p>Selected file: ${selectedFile.name}</p>
                <p style="color: red; text-align: center;">Error: ${error}</p>
            `;
        });
    });

    function displayResults(data) {
        const isNSFW = data.nsfw_status.includes("NSFW");
        const statusClass = isNSFW ? 'unsafe' : 'safe';
        
        resultContent.innerHTML = `
            <p>Selected file: ${selectedFile.name}</p>
            <div class="result-status ${statusClass}">
                ${data.nsfw_status}
            </div>
            <div class="result-details">
                <h4>Analysis Details</h4>
                <div class="result-item">
                    <span>${data.highest_category}</span>
                    <span>${data.highest_percentage}</span>
                </div>
            </div>
        `;
    }
});