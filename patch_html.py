import re

with open('app/src/main/assets/index.html', 'r') as f:
    html = f.read()

# Replace updateBtn onclick
# Previous: onclick="window.location.href=window.updateLink"
html = re.sub(
    r'onclick="window.location.href=window.updateLink"',
    r'''onclick="if(window.AndroidUpdater){window.AndroidUpdater.startUpdate(window.updateLink)}else{window.location.href=window.updateLink}"''',
    html
)

with open('app/src/main/assets/index.html', 'w') as f:
    f.write(html)
