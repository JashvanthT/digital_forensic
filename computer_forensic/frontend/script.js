// Backend URL - adjust if your backend runs on a different port
const BACKEND_URL = "http://127.0.0.1:5000";

let progressInterval = null;

function submitImage() {
  const fileInput = document.getElementById('diskImage');
  const file = fileInput.files[0];
  const selectedDBs = Array.from(document.querySelectorAll('.db-options input:checked')).map(cb => cb.value);

  if (!file) {
    alert("Please select a disk image file (.E01, .001, .dd, or .img)");
    return;
  }

  // Validate file extension
  const validExtensions = ['.e01', '.001', '.dd', '.img'];
  const fileName = file.name.toLowerCase();
  const isValid = validExtensions.some(ext => fileName.endsWith(ext));
  
  if (!isValid) {
    alert("Invalid file type. Please select a .E01, .001, .dd, or .img file.");
    return;
  }

  // Show progress bar
  showProgressBar();
  updateProgress(0, "Uploading file...");

  const formData = new FormData();
  formData.append("image", file);
  formData.append("databases", JSON.stringify(selectedDBs));

  fetch(`${BACKEND_URL}/upload-image`, {
    method: "POST",
    body: formData
  })
  .then(res => {
    if (!res.ok) {
      return res.json().then(err => {
        throw new Error(err.error || "Upload failed");
      });
    }
    return res.json();
  })
  .then(data => {
    if (data.success && data.job_id) {
      // Start polling for job status
      pollJobStatus(data.job_id);
    } else {
      hideProgressBar();
      alert("Upload failed: " + (data.error || "Unknown error"));
    }
  })
  .catch(err => {
    hideProgressBar();
    console.error("Upload failed:", err);
    alert("Upload failed: " + err.message);
  });
}

function pollJobStatus(jobId) {
  progressInterval = setInterval(() => {
    fetch(`${BACKEND_URL}/job-status/${jobId}`)
      .then(res => res.json())
      .then(data => {
        updateProgress(data.progress, data.message);
        
        if (data.status === "completed") {
          clearInterval(progressInterval);
          hideProgressBar();
          
          if (data.result) {
            alert(`✓ Extraction complete!\n${data.result.message}`);
            loadCaseDetails(data.result.caseDetails);
            loadRecentFiles(data.result.recentFiles);
          }
        } else if (data.status === "error") {
          clearInterval(progressInterval);
          hideProgressBar();
          alert("Extraction failed: " + (data.error || "Unknown error"));
        }
      })
      .catch(err => {
        clearInterval(progressInterval);
        hideProgressBar();
        console.error("Status check failed:", err);
        alert("Failed to check extraction status");
      });
  }, 1000); // Poll every second
}

function showProgressBar() {
  let progressSection = document.getElementById('progressSection');
  if (!progressSection) {
    progressSection = document.createElement('div');
    progressSection.id = 'progressSection';
    progressSection.className = 'progress-section';
    progressSection.innerHTML = `
      <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
      </div>
      <div class="progress-text" id="progressText">Starting...</div>
    `;
    document.querySelector('.upload-section').appendChild(progressSection);
  }
  progressSection.style.display = 'block';
}

function hideProgressBar() {
  const progressSection = document.getElementById('progressSection');
  if (progressSection) {
    progressSection.style.display = 'none';
  }
}

function updateProgress(percent, message) {
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  
  if (progressBar) {
    progressBar.style.width = percent + '%';
  }
  if (progressText) {
    progressText.textContent = message || `${percent}%`;
  }
}

function loadCaseDetails(details) {
  document.getElementById("spaceInfo").textContent = details.space || "N/A";
  document.getElementById("fsInfo").textContent = details.fileSystem || "N/A";
  document.getElementById("hashInfo").textContent = details.hash || "N/A";
  document.getElementById("keysInfo").textContent = Array.isArray(details.keys) ? details.keys.join(", ") : details.keys || "N/A";
  document.getElementById("totalFiles").textContent = details.totalFiles || 0;
}

function loadRecentFiles(files) {
  const container = document.getElementById("recentFiles");
  if (!files || files.length === 0) {
    container.innerHTML = "<div>No recent files found</div>";
    return;
  }
  container.innerHTML = files.map(f => `<div class="file-item">📄 ${f}</div>`).join("");
}

let currentChart = null;

function loadPlot(type) {
  // Disable all plot buttons during loading
  const buttons = document.querySelectorAll('.plot-tabs button');
  buttons.forEach(btn => btn.disabled = true);
  
  fetch(`${BACKEND_URL}/plots?type=${type}`)
    .then(res => {
      if (!res.ok) {
        return res.json().then(err => {
          throw new Error(err.error || "Plot fetch failed");
        });
      }
      return res.json();
    })
    .then(data => {
      buttons.forEach(btn => btn.disabled = false);
      
      if (data.error) {
        alert(data.error);
        return;
      }
      
      const ctx = document.getElementById("plotCanvas").getContext("2d");
      if (currentChart) {
        currentChart.destroy();  // Clear old chart
      }
      
      // Determine chart type
      let chartType = "bar";
      if (type === "pie") chartType = "pie";
      else if (type === "line") chartType = "line";
      else if (type === "histogram") chartType = "bar";
      
      currentChart = new Chart(ctx, {
        type: chartType,
        data: data.chartData,
        options: data.chartOptions
      });
    })
    .catch(err => {
      buttons.forEach(btn => btn.disabled = false);
      console.error("Plot load failed:", err);
      alert("Failed to load plot: " + err.message);
    });
}

