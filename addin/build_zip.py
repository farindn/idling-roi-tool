#!/usr/bin/env python3
"""
Build the Idling ROI Tool as a MyGeotab add-in ZIP.

Usage: python build_zip.py   (run from the addin/ directory)
Output: releases/idling-roi-tool.zip

MyGeotab's add-in context blocks inline <style> tags (CSP) and external CDN
requests, so:
  - The inline CSS is extracted into main.css (linked stylesheet)
  - Chart.js and the Material Symbols font are downloaded and bundled

ZIP structure:
  configuration.json
  Idling ROI Tool/
    index.html                         (patched — <style> -> <link>, local refs)
    main.css                           (extracted CSS + @font-face)
    chart.js                           (bundled from CDN)
    material-symbols-rounded.woff2     (bundled from Google Fonts)
    geotab-logo(full-colour-rgb).png
"""

import base64
import json
import re
import urllib.request
import zipfile
from pathlib import Path

ROOT         = Path(__file__).parent
PROJECT_ROOT = ROOT.parent
RELEASES     = ROOT / "releases"
ADDIN_FOLDER = "Idling ROI Tool"

CHARTJS_URL = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"

MATERIAL_SYMBOLS_CSS_URL = (
    "https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:"
    "opsz,wght,FILL,GRAD@24,400,0,0&display=block"
)

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": BROWSER_UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def get_material_symbols():
    """Download Material Symbols woff2; return (bytes, font-face CSS for local ref)."""
    print("  Fetching Material Symbols CSS from Google Fonts...")
    css = fetch(MATERIAL_SYMBOLS_CSS_URL).decode("utf-8")

    match = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)", css)
    if not match:
        raise RuntimeError("Could not find woff2 URL in Material Symbols CSS response.")

    woff2_url = match.group(1)
    print(f"  Downloading font: {woff2_url[:80]}...")
    woff2_bytes = fetch(woff2_url)
    print(f"  Font size: {len(woff2_bytes) / 1024:.0f} KB")

    font_face = (
        "@font-face {\n"
        "  font-family: 'Material Symbols Rounded';\n"
        "  font-style: normal;\n"
        "  font-weight: 100 700;\n"
        "  font-display: block;\n"
        "  src: url('material-symbols-rounded.woff2') format('woff2');\n"
        "}"
    )
    return woff2_bytes, font_face


def patch_html(html):
    """
    Patch the HTML for the add-in context. Returns (patched_html, extracted_css).

    - Extracts the inline <style> block into a separate string (-> main.css)
    - Replaces <style>...</style> with <link rel="stylesheet" href="main.css">
    - Removes Google Fonts preconnect and stylesheet links
    - Replaces CDN Chart.js <script> with local reference
    """
    # Remove Google Fonts preconnect hints
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', "", html)

    # Remove Google Fonts stylesheet links (IBM Plex Sans/Mono + Material Symbols)
    html = re.sub(r'<link href="https://fonts\.googleapis\.com[^"]*"[^>]*>\s*', "", html)

    # Replace CDN Chart.js script with local copy
    html = re.sub(
        r'<script src="https://cdn\.jsdelivr\.net/npm/chart\.js[^"]*"></script>',
        '<script src="chart.js"></script>',
        html,
    )

    # Extract the inline <style> block and replace with <link> — must run AFTER
    # the re.sub calls above so positions in style_match reflect the current html.
    style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    css_content = style_match.group(1) if style_match else ""
    if style_match:
        html = (
            html[: style_match.start()]
            + '<link rel="stylesheet" href="main.css">'
            + html[style_match.end() :]
        )

    return html, css_content


def main():
    print("Building ZIP archive...")

    # --- Icon for configuration.json ---
    icon_bytes    = (ROOT / "icon.svg").read_bytes()
    icon_data_uri = f"data:image/svg+xml;base64,{base64.b64encode(icon_bytes).decode()}"

    config = {
        "name":         "Idling ROI Tool",
        "supportEmail": "farinnugraha@geotab.com",
        "version":      "1.0.0",
        "items": [
            {
                "version":  "1.0.0",
                "url":      f"/{ADDIN_FOLDER}/index.html",
                "category": "ReportsId",
                "menuName": {"en": "Idling ROI Tool"},
                "icon":     icon_data_uri,
            }
        ],
    }

    # --- Download external assets ---
    print("  Downloading Chart.js...")
    chartjs_bytes = fetch(CHARTJS_URL)
    print(f"  Chart.js size: {len(chartjs_bytes) / 1024:.0f} KB")

    material_symbols_bytes, font_face = get_material_symbols()

    # --- Patch HTML and extract CSS ---
    html_src          = (ROOT / "index.html").read_text(encoding="utf-8")
    html_out, css_out = patch_html(html_src)
    css_out           = css_out + f"\n{font_face}\n"   # append @font-face

    logo_src = PROJECT_ROOT / "geotab-logo(full-colour-rgb).png"

    # --- Assemble ZIP ---
    RELEASES.mkdir(parents=True, exist_ok=True)
    zip_path = RELEASES / "idling-roi-tool.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("configuration.json",                       json.dumps(config, indent=2))
        zf.writestr(f"{ADDIN_FOLDER}/index.html",               html_out)
        zf.writestr(f"{ADDIN_FOLDER}/main.css",                 css_out)
        zf.writestr(f"{ADDIN_FOLDER}/chart.js",                 chartjs_bytes.decode("utf-8"))
        zf.writestr(f"{ADDIN_FOLDER}/material-symbols-rounded.woff2",
                    material_symbols_bytes)
        zf.write(logo_src, f"{ADDIN_FOLDER}/geotab-logo(full-colour-rgb).png")

    print(f"\nCreated: {zip_path}  ({zip_path.stat().st_size / 1024:.0f} KB)")
    print("\nZIP contents:")
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            size_kb = info.file_size / 1024
            print(f"  {info.filename:<55} ({size_kb:.0f} KB)")

    print("\nTo install:")
    print("  MyGeotab -> Administration -> System -> System Settings -> Add-Ins")
    print("  -> New Add-In -> upload releases/idling-roi-tool.zip -> OK -> Save -> Refresh")
    print("  -> Find under Reports -> Idling ROI Tool")


if __name__ == "__main__":
    main()
