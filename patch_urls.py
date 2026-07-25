import os

for html_file in ["app/src/main/assets/index.html", "app/src/main/assets/result.html"]:
    with open(html_file, "r") as f:
        content = f.read()
    
    if html_file == "app/src/main/assets/result.html":
        # Replace empty fallback with the new fallback
        old_code = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "";'
        new_code = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://all-number-info-rajan-eta.vercel.app/api?number=";'
        content = content.replace(old_code, new_code)
        
        # Also replace the old vercel url if it's still there somehow
        old_code2 = 'let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://numberinfobysatyam.vercel.app/?apikey=satyam&number=";'
        content = content.replace(old_code2, new_code)

    with open(html_file, "w") as f:
        f.write(content)
print("Patched URLs")
