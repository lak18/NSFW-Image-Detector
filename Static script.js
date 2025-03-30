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
                <p>Note: This is a static demo. In the GitHub Pages version, we can only show a mock result.</p>
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

        // Generate mock results since we can't run the actual detection on GitHub Pages
        setTimeout(() => {
            clearInterval(interval);
            progressBar.style.width = '100%';
            
            // Mock data for demonstration
            const mockData = {
                highest_category: "neutral",
                highest_percentage: "95.2%",
                nsfw_status: "It is not a NSFW image",
                categories: {
                    "drawings": 0.023,
                    "hentai": 0.001,
                    "neutral": 0.952,
                    "porn": 0.004,
                    "sexy": 0.02
                }
            };
            
            // Process the mock data
            setTimeout(() => {
                displayResults(mockData);
            }, 500);
        }, 2000);
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
                <p style="margin-top: 20px; color: #666; text-align: center;">
                    Note: This is a static demo. For real NSFW detection, please run the Flask app locally.
                </p>
            </div>
        `;
    }
});
