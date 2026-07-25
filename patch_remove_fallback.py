import os

RESULT_PATH = "app/src/main/assets/result.html"

with open(RESULT_PATH, "r") as f:
    result_html = f.read()

old_code = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://numberinfobysatyam.vercel.app/?apikey=satyam&number=";'
new_code = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "";'

if old_code in result_html:
    result_html = result_html.replace(old_code, new_code)
    with open(RESULT_PATH, "w") as f:
        f.write(result_html)
    print("Removed fallback from result.html")
else:
    print("Old code not found in result.html")
