'''List files from a directory and its subdirectories recursively sorted by time and generate an HTML file'''

import os
import sys
import html
from datetime import datetime

# Take target directory as an argument
if len(sys.argv) < 2:
    print("Usage: python3 generate_file_list_html.py <target_directory> [output_file]")
    sys.exit(1)

target_dir = sys.argv[1]
output_filename = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/Desktop/files_sorted_by_time.html')

files_with_times = []
try:
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            path = os.path.join(root, name)
            ts = os.path.getmtime(path)
            rel_path = os.path.relpath(path, start=target_dir)
            files_with_times.append((ts, rel_path))
except Exception as e:
    print(f"Error occurred: {e}")
    sys.exit(1)

files_with_times.sort(key=lambda x: x[0], reverse=True)

html_content = '<html><head><title>Files Sorted by Modification Time</title></head><body>'
html_content += f'<h1>Files in {html.escape(target_dir)} Sorted by Modification Time</h1><ul>'

for ts, filepath in files_with_times:
    date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    file_link = html.escape(filepath)
    html_content += f'<li><a href="file://{file_link}" target="_blank" rel="noopener noreferrer">{file_link}</a> - {date_str}</li>'

html_content += '</ul></body></html>'

try:
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML file created: {output_filename}")
except Exception as e:
    print(f"Error occurred while writing the HTML file: {e}")