import os

RESULT_PATH = "app/src/main/assets/result.html"

with open(RESULT_PATH, "r") as f:
    content = f.read()

old_code = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://all-number-info-rajan-eta.vercel.app/api?number=";'
new_code = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "";'

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(RESULT_PATH, "w") as f:
        f.write(content)
    print("Fallback removed.")
else:
    print("Target string not found!")
