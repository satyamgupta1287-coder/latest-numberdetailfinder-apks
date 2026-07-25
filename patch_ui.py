import os
import re

INDEX_PATH = "app/src/main/assets/index.html"
RESULT_PATH = "app/src/main/assets/result.html"

with open(INDEX_PATH, "r") as f:
    index_html = f.read()

update_modal_html = """
<div id="updateModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(4,7,10,0.9); z-index:9999; justify-content:center; align-items:center; flex-direction:column; padding:20px;">
  <div style="background:#070d10; border:1px solid #38e8ff; border-radius:12px; padding:30px; text-align:center; max-width:400px;">
    <h2 style="color:#22ff9c; font-family:'JetBrains Mono', monospace; margin-top:0;">UPDATE REQUIRED</h2>
    <p style="color:#5affb9; font-family:'Space Grotesk', sans-serif; font-size:14px; margin-bottom:24px;">A new version of Cyber Trace X is available. Please update to continue using the system.</p>
    <button id="updateBtn" style="background:#38e8ff; color:#000; border:none; padding:15px 30px; font-family:'JetBrains Mono', monospace; font-weight:bold; border-radius:8px; cursor:pointer; width:100%; font-size:16px;" onclick="window.location.href=window.updateLink">UPDATE NOW</button>
  </div>
</div>
"""

update_script = """
/* CONFIG UPDATE CHECK */
const CONFIG_URL = "https://raw.githubusercontent.com/satyamgupta1287-coder/numberdetailfinder/main/app_config.json?t=" + Date.now();
const APP_VERSION = 1;

async function checkConfig() {
  try {
    let res = await fetch(CONFIG_URL);
    if (!res.ok) return;
    let config = await res.json();
    
    if (config.api_url) {
      localStorage.setItem("DYNAMIC_API_URL", config.api_url);
    }
    
    if (config.version > APP_VERSION) {
      window.updateLink = config.update_url || "https://github.com/satyamgupta1287-coder/numberdetailfinder";
      document.getElementById('updateModal').style.display = 'flex';
      document.getElementById('number').disabled = true;
      document.getElementById('traceBtn').disabled = true;
    }
  } catch (e) {
    console.log("Config check failed", e);
  }
}
window.addEventListener('load', checkConfig);
"""

# Inject into index.html
if "updateModal" not in index_html:
    index_html = index_html.replace("<body>", f"<body>{update_modal_html}")
    index_html = index_html.replace("/* sound */", f"{update_script}\n/* sound */")
    with open(INDEX_PATH, "w") as f:
        f.write(index_html)


with open(RESULT_PATH, "r") as f:
    result_html = f.read()

# Replace hardcoded fetch in result.html
old_fetch = 'const res = await fetch("https://numberinfobysatyam.vercel.app/?apikey=satyam&number=" + encodeURIComponent(num));'
new_fetch = """
    let baseUrl = localStorage.getItem("DYNAMIC_API_URL") || "https://numberinfobysatyam.vercel.app/?apikey=satyam&number=";
    const res = await fetch(baseUrl + encodeURIComponent(num));
"""

if "DYNAMIC_API_URL" not in result_html:
    result_html = result_html.replace(old_fetch, new_fetch)
    with open(RESULT_PATH, "w") as f:
        f.write(result_html)

print("UI Patched successfully")
