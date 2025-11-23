def build_features(parsed_data):
    """
    Convert raw parsed data into structured features for storage and visualization
    """
    if "error" in parsed_data:
        return parsed_data
    
    # Extract and structure features
    features = {
        "filename": parsed_data.get("filename", "unknown"),
        "recent_files": parsed_data.get("recent_files", []),
        "space": parsed_data.get("space", "N/A"),
        "file_system": parsed_data.get("file_system", "Unknown"),
        "hash": parsed_data.get("hash", "N/A"),
        "keys": parsed_data.get("keys", []),
        "total_files": parsed_data.get("total_files", 0),
        "file_types": parsed_data.get("file_types", {}),
        "size_bytes": parsed_data.get("size_bytes", 0)
    }
    
    return features
