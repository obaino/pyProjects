'''list files from a directory and its subdirectories recursively sorted by time and generate
    an html file'''

import os
import sys
from datetime import datetime

# take target directory as an argument
#
# if len(sys.argv) < 2:
#     print("Usage: python3 generate_file_list_html.py <target_directory>")
#     sys.exit(1)

# target_dir = sys.argv[1]

# Set the target directory
target_dir = '/media/nikolask/2T_BackUp/Archived/Phd_Docs'

files_with_times = []
for root, dirs, files in os.walk(target_dir):
    for name in files:
        path = os.path.join(root, name)
        ts = os.path.getmtime(path)
        # rel_path = os.path.relpath(path, start=target_dir)
        # files_with_times.append((ts, rel_path))
        abs_path = os.path.abspath(path)
        files_with_times.append((ts, abs_path))


files_with_times.sort(key=lambda x: x[0], reverse=True)

html_content = '<html><head><title>Files Sorted by Modification Time</title></head><body>'
html_content += f'<h1>Files in {target_dir} Sorted by Modification Time</h1><ul>'

for ts, filepath in files_with_times:
    date_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    html_content += f'<li><a href="file://{filepath}" target="_blank" rel="noopener noreferrer">{filepath}</a> - {date_str}</li>'

html_content += '</ul></body></html>'

output_filename = os.path.expanduser('~/Desktop/3X_files.html')
with open(output_filename, 'w') as f:
    f.write(html_content)


print(f"HTML file created: {output_filename}")
