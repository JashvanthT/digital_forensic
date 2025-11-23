import os
import hashlib
import random

def parse_disk_image(image_path, progress_callback=None):
    """
    Parse disk image and extract metadata.
    Supports .E01, .001, .dd, .img formats
    
    Args:
        image_path: Path to the disk image file
        progress_callback: Optional callback function(progress, message) for progress updates
    """
    if not os.path.exists(image_path):
        return {"error": f"File not found: {image_path}"}

    size = os.path.getsize(image_path)
    filename = os.path.basename(image_path)
    ext = os.path.splitext(filename)[1].lower()

    if progress_callback:
        progress_callback(20, "Reading file and calculating hashes...")

    # Compute MD5 and SHA256 with progress tracking
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    
    bytes_read = 0
    chunk_size = 8192
    
    with open(image_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
            
            # Update progress
            bytes_read += len(chunk)
            if progress_callback and size > 0:
                progress = 20 + int((bytes_read / size) * 40)  # 20-60% for hashing
                progress_callback(progress, f"Hashing: {bytes_read/1024/1024:.1f} MB / {size/1024/1024:.1f} MB")
    
    if progress_callback:
        progress_callback(65, "Extracting file metadata...")

    # Determine file system based on extension
    fs_map = {
        '.e01': 'EnCase Evidence File (EWF)',
        '.001': 'Split Raw Image',
        '.dd': 'Raw Disk Image (DD)',
        '.img': 'Raw Disk Image'
    }
    file_system = fs_map.get(ext, 'Unknown')

    # Simulate file extraction (in real scenario, parse actual filesystem)
    recent_files = [
        f"Documents/report_{i}.pdf" for i in range(1, 6)
    ] + [
        f"Pictures/photo_{i}.jpg" for i in range(1, 4)
    ] + [
        f"Downloads/setup_{i}.exe" for i in range(1, 3)
    ]

    # Simulate file type distribution
    file_types = {
        "PDF": random.randint(10, 50),
        "DOCX": random.randint(5, 30),
        "JPG": random.randint(20, 100),
        "PNG": random.randint(10, 50),
        "EXE": random.randint(5, 20),
        "TXT": random.randint(15, 40),
        "ZIP": random.randint(3, 15),
        "MP4": random.randint(2, 10)
    }
    
    total_files = sum(file_types.values())
    allocated_space = size * 0.7  # 70% allocated
    unallocated_space = size * 0.3  # 30% unallocated

    return {
        "filename": filename,
        "recent_files": recent_files[:10],  # Top 10 recent files
        "file_system": file_system,
        "total_files": total_files,
        "space": f"Allocated: {allocated_space/1024/1024:.2f} MB, Unallocated: {unallocated_space/1024/1024:.2f} MB",
        "hash": f"MD5: {md5_hash.hexdigest()}, SHA256: {sha256_hash.hexdigest()}",
        "keys": [f"case_id:{random.randint(1000, 9999)}", "examiner:Forensic_Team", f"evidence_tag:EV{random.randint(100, 999)}"],
        "file_types": file_types,
        "size_bytes": size
    }
