import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    manifest = f.read()

# Add attribution tag if not present
if "<attribution" not in manifest:
    manifest = manifest.replace("<application", '<attribution android:tag="WebView" android:label="@string/app_name" />\n    <application')
    
with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(manifest)
print("Patched manifest")
