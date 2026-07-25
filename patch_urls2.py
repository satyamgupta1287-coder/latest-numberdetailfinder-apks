import os

for html_file in ["app/src/main/assets/index.html", "app/src/main/assets/result.html"]:
    with open(html_file, "r") as f:
        content = f.read()
    
    old_code = "https://raw.githubusercontent.com/satyamgupta1287-coder/numberdetailfinder/main/app_config.json"
    new_code = "https://raw.githubusercontent.com/satyamgupta1287-coder/numberdetailfinder-apk/refs/heads/main/app_config.json"
    
    content = content.replace(old_code, new_code)

    with open(html_file, "w") as f:
        f.write(content)
print("Patched GitHub URLs successfully")
