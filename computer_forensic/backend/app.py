from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import threading
import time
import uuid

# Import your existing modules
from feature_builder.feature_builder import build_features
from extraction.extractor import parse_disk_image
from backend.db_router import insert_to_db
from backend.plot_builder import (
    generate_histogram,
    generate_bar_chart,
    generate_pie_chart,
    generate_line_chart
)

app = Flask(__name__)
CORS(app)
last_features = {}
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store job status and results
jobs = {}

class ExtractionJob:
    def __init__(self, job_id, filename):
        self.job_id = job_id
        self.filename = filename
        self.status = "uploading"  # uploading, processing, completed, error
        self.progress = 0
        self.message = "Uploading file..."
        self.result = None
        self.error = None

def process_extraction(job_id, image_path, databases):
    """Background task to process file extraction"""
    job = jobs[job_id]
    
    try:
        # Update status
        job.status = "processing"
        job.progress = 10
        job.message = "Calculating file hashes..."
        
        # Extract data using extractor.py
        print(f"Parsing disk image: {image_path}")
        parsed_data = parse_disk_image(image_path, progress_callback=lambda p, m: update_progress(job_id, p, m))
        
        if "error" in parsed_data:
            job.status = "error"
            job.error = parsed_data["error"]
            return
        
        job.progress = 70
        job.message = "Building features..."
        
        # Build features
        features = build_features(parsed_data)
        
        # Save features globally so plots can use them
        global last_features
        last_features = features
        
        job.progress = 80
        job.message = "Storing in databases..."
        
        # Insert into selected databases
        for db in databases:
            try:
                print(f"Inserting data into {db}")
                insert_to_db(db, features)
            except Exception as e:
                print(f"Error inserting to {db}: {str(e)}")
        
        job.progress = 100
        job.status = "completed"
        job.message = "Extraction completed!"
        
        # Prepare result
        job.result = {
            "success": True,
            "message": f"Extracted data from {os.path.basename(image_path)}",
            "caseDetails": {
                "space": features.get("space", "N/A"),
                "fileSystem": features.get("file_system", "N/A"),
                "hash": features.get("hash", "N/A"),
                "keys": features.get("keys", []),
                "totalFiles": features.get("total_files", 0)
            },
            "recentFiles": features.get("recent_files", [])
        }
        
    except Exception as e:
        print(f"Error in process_extraction: {str(e)}")
        job.status = "error"
        job.error = str(e)

def update_progress(job_id, progress, message):
    """Update job progress"""
    if job_id in jobs:
        jobs[job_id].progress = progress
        jobs[job_id].message = message

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """
    Handle disk image upload and start background extraction
    """
    try:
        # Get uploaded file
        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        image = request.files['image']
        if image.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Get selected databases
        databases_json = request.form.get('databases', '[]')
        databases = json.loads(databases_json)
        
        # Create unique job ID
        job_id = str(uuid.uuid4())
        
        # Save uploaded file
        image_path = os.path.join(UPLOAD_FOLDER, image.filename)
        image.save(image_path)
        
        # Create job
        job = ExtractionJob(job_id, image.filename)
        jobs[job_id] = job
        
        # Start background processing
        thread = threading.Thread(target=process_extraction, args=(job_id, image_path, databases))
        thread.daemon = True
        thread.start()
        
        # Return job ID immediately
        return jsonify({
            "success": True,
            "job_id": job_id,
            "message": "Upload successful, processing started"
        })
    
    except Exception as e:
        print(f"Error in upload_image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/job-status/<job_id>', methods=['GET'])
def job_status(job_id):
    """Get the status of an extraction job"""
    if job_id not in jobs:
        return jsonify({"error": "Job not found"}), 404
    
    job = jobs[job_id]
    
    response = {
        "job_id": job_id,
        "status": job.status,
        "progress": job.progress,
        "message": job.message
    }
    
    if job.status == "completed" and job.result:
        response["result"] = job.result
    elif job.status == "error":
        response["error"] = job.error
    
    return jsonify(response)


@app.route('/plots', methods=['GET'])
def plots():
    """
    Generate plot data based on extracted features
    """
    plot_type = request.args.get('type')
    global last_features

    if not last_features or not last_features.get("file_types"):
        return jsonify({
            "error": "No data available. Please upload a disk image first."
        }), 400

    try:
        if plot_type == "histogram":
            return jsonify(generate_histogram(last_features))
        elif plot_type == "bar":
            return jsonify(generate_bar_chart(last_features))
        elif plot_type == "pie":
            return jsonify(generate_pie_chart(last_features))
        elif plot_type == "line":
            return jsonify(generate_line_chart(last_features))
        else:
            return jsonify({"error": "Invalid plot type"}), 400
    except Exception as e:
        print(f"Error generating plot: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
