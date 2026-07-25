import os

RESULT_PATH = "app/src/main/assets/result.html"

with open(RESULT_PATH, "r") as f:
    result_html = f.read()

old_code = """
    let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://numberinfobysatyam.vercel.app/?apikey=satyam&number=";
"""
new_code = """
    let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://numberinfobysatyam.vercel.app/?apikey=satyam&number=";
    try {
        let confRes = await fetch("https://raw.githubusercontent.com/satyamgupta1287-coder/numberdetailfinder/main/app_config.json?t=" + Date.now());
        if (confRes.ok) {
            let conf = await confRes.json();
            if (conf.api_url) {
                baseUrl = conf.api_url;
                localStorage.setItem("DYNAMIC_API_URL", conf.api_url);
            }
        }
    } catch(e) {
        console.log("Config fetch in result failed:", e);
    }
"""

if old_code in result_html:
    result_html = result_html.replace(old_code, new_code)
    with open(RESULT_PATH, "w") as f:
        f.write(result_html)
    print("Patched result.html")
else:
    print("Old code not found in result.html")
