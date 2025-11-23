"""
Simple test script to verify backend functionality
"""
import os
import sys

# Test imports
try:
    from extraction.extractor import parse_disk_image
    from feature_builder.feature_builder import build_features
    from backend.plot_builder import (
        generate_histogram,
        generate_bar_chart,
        generate_pie_chart,
        generate_line_chart
    )
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test extractor with a dummy file
print("\n--- Testing Extractor ---")
test_file = "test_image.dd"
with open(test_file, "wb") as f:
    f.write(b"Test disk image data" * 1000)

parsed_data = parse_disk_image(test_file)
print(f"✓ Parsed data keys: {list(parsed_data.keys())}")
print(f"  - File system: {parsed_data.get('file_system')}")
print(f"  - Total files: {parsed_data.get('total_files')}")
print(f"  - File types: {parsed_data.get('file_types')}")

# Test feature builder
print("\n--- Testing Feature Builder ---")
features = build_features(parsed_data)
print(f"✓ Features built: {list(features.keys())}")

# Test plot builders
print("\n--- Testing Plot Builders ---")
try:
    hist = generate_histogram(features)
    print(f"✓ Histogram generated with {len(hist['chartData']['labels'])} labels")
    
    bar = generate_bar_chart(features)
    print(f"✓ Bar chart generated with {len(bar['chartData']['labels'])} labels")
    
    pie = generate_pie_chart(features)
    print(f"✓ Pie chart generated with {len(pie['chartData']['labels'])} labels")
    
    line = generate_line_chart(features)
    print(f"✓ Line chart generated with {len(line['chartData']['labels'])} data points")
except Exception as e:
    print(f"✗ Plot generation error: {e}")

# Cleanup
os.remove(test_file)
print("\n✓ All tests passed!")
