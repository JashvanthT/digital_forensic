# Digital Forensic Triage Dashboard - Usage Guide

## Overview
This system allows you to upload disk images, extract forensic data, store it in databases, and visualize the results.

## Supported File Types
- `.E01` - EnCase Evidence File (EWF)
- `.001` - Split Raw Image
- `.dd` - Raw Disk Image (DD)
- `.img` - Raw Disk Image

## How to Use

### 1. Start the Backend Server
```bash
cd computer_forensic
python backend/app.py
```
The server will start on `http://127.0.0.1:5000`

### 2. Open the Frontend
Open `frontend/index.html` in your web browser.

### 3. Upload a Disk Image
1. Click "Choose File" and select a disk image (.E01, .001, .dd, or .img)
2. Select which databases you want to store the data in:
   - MongoDB
   - PostgreSQL
   - Neo4j
   - VectorDB
3. Click "Extract & Store"

### 4. View Results
After extraction completes:
- **Case Details** section shows:
  - Allocated/Unallocated space
  - File system type
  - MD5 and SHA256 hashes
  - Evidence keys
  - Total file count

- **Recent Accessed Files** section displays the most recently accessed files

### 5. Generate Visualizations
Click any of the plot buttons to visualize the data:
- **Histogram** - Bar chart showing file type distribution
- **Bar Chart** - Horizontal comparison of file types
- **Pie Chart** - Proportional view of file types
- **Scatter Plot** - Distribution plot of file types

## Data Flow
1. **Upload** → File saved to `uploads/` folder
2. **Extract** → `extractor.py` parses the disk image
3. **Build Features** → `feature_builder.py` structures the data
4. **Store** → `db_router.py` saves to selected databases
5. **Visualize** → `plot_builder.py` generates chart data
6. **Display** → Frontend renders results and charts

## Troubleshooting
- If plots don't load, make sure you've uploaded a file first
- Check browser console (F12) for any JavaScript errors
- Check backend terminal for Python errors
- Ensure all required Python packages are installed: `pip install -r requirements.txt`
