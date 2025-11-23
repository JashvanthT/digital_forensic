def generate_histogram(features):
    """Generate histogram data from file types"""
    file_types = features.get("file_types", {})
    if not file_types:
        file_types = {"No Data": 0}
    
    labels = list(file_types.keys())
    values = list(file_types.values())
    
    # Generate colors for each file type
    colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    return {
        'chartData': {
            'labels': labels,
            'datasets': [{
                'label': 'File Count',
                'data': values,
                'backgroundColor': colors[:len(labels)],
                'borderColor': colors[:len(labels)],
                'borderWidth': 1
            }]
        },
        'chartOptions': {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {'display': False},
                'title': {'display': True, 'text': 'File Type Distribution (Histogram)'}
            },
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {'display': True, 'text': 'Number of Files'}
                },
                'x': {
                    'title': {'display': True, 'text': 'File Type'}
                }
            }
        }
    }

    
def generate_bar_chart(features):
    """Generate bar chart data from file types"""
    file_types = features.get("file_types", {})
    if not file_types:
        file_types = {"No Data": 0}
    
    labels = list(file_types.keys())
    values = list(file_types.values())
    
    colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    return {
        'chartData': {
            'labels': labels,
            'datasets': [{
                'label': 'File Count',
                'data': values,
                'backgroundColor': colors[:len(labels)],
                'borderColor': colors[:len(labels)],
                'borderWidth': 2
            }]
        },
        'chartOptions': {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {'display': True, 'position': 'top'},
                'title': {'display': True, 'text': 'File Type Distribution (Bar Chart)'}
            },
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {'display': True, 'text': 'Number of Files'}
                }
            }
        }
    }


def generate_pie_chart(features):
    """Generate pie chart data from file types"""
    file_types = features.get("file_types", {})
    if not file_types:
        file_types = {"No Data": 0}
    
    labels = list(file_types.keys())
    values = list(file_types.values())
    
    colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
    ]

    return {
        'chartData': {
            'labels': labels,
            'datasets': [{
                'data': values,
                'backgroundColor': colors[:len(labels)],
                'borderColor': '#ffffff',
                'borderWidth': 2
            }]
        },
        'chartOptions': {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {'display': True, 'position': 'right'},
                'title': {'display': True, 'text': 'File Type Distribution (Pie Chart)'}
            }
        }
    }

def generate_line_chart(features):
    """Generate line chart data from file types"""
    file_types = features.get("file_types", {})
    if not file_types:
        file_types = {"No Data": 0}
    
    labels = list(file_types.keys())
    values = list(file_types.values())

    return {
        'chartData': {
            'labels': labels,
            'datasets': [{
                'label': 'File Count Trend',
                'data': values,
                'backgroundColor': 'rgba(102, 126, 234, 0.2)',
                'borderColor': '#667eea',
                'borderWidth': 3,
                'fill': True,
                'tension': 0.4,
                'pointRadius': 5,
                'pointHoverRadius': 7,
                'pointBackgroundColor': '#667eea',
                'pointBorderColor': '#fff',
                'pointBorderWidth': 2
            }]
        },
        'chartOptions': {
            'responsive': True,
            'maintainAspectRatio': True,
            'plugins': {
                'legend': {'display': True, 'position': 'top'},
                'title': {'display': True, 'text': 'File Type Distribution (Line Chart)'}
            },
            'scales': {
                'y': {
                    'beginAtZero': True,
                    'title': {'display': True, 'text': 'Number of Files'},
                    'grid': {
                        'color': 'rgba(0, 0, 0, 0.1)'
                    }
                },
                'x': {
                    'title': {'display': True, 'text': 'File Type'},
                    'grid': {
                        'display': False
                    }
                }
            }
        }
    }
