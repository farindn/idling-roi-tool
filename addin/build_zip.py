#!/usr/bin/env python3
"""
Build the Idling ROI Tool as a MyGeotab add-in ZIP.

Usage: python build_zip.py   (run from the addin/ directory)
Output: releases/idling-roi-tool.zip

ZIP structure:
  configuration.json
  Idling ROI Tool/
    index.html
    geotab-logo(full-colour-rgb).png
"""

import base64
import json
import zipfile
from pathlib import Path

ROOT         = Path(__file__).parent
PROJECT_ROOT = ROOT.parent
RELEASES     = ROOT / "releases"
ADDIN_FOLDER = "Idling ROI Tool"


def main():
    print("Building ZIP archive...")

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
                "icon":     icon_data_uri
            }
        ]
    }

    RELEASES.mkdir(parents=True, exist_ok=True)
    zip_path = RELEASES / "idling-roi-tool.zip"

    logo_src = PROJECT_ROOT / "geotab-logo(full-colour-rgb).png"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("configuration.json", json.dumps(config, indent=2))
        zf.write(ROOT / "index.html", f"{ADDIN_FOLDER}/index.html")
        zf.write(logo_src,            f"{ADDIN_FOLDER}/geotab-logo(full-colour-rgb).png")

    print(f"\nCreated: {zip_path}  ({zip_path.stat().st_size / 1024:.1f} KB)")
    print("\nZIP contents:")
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            print(f"  {info.filename}")

    print("\nTo install:")
    print("  MyGeotab -> Administration -> System -> System Settings -> Add-Ins")
    print("  -> New Add-In -> upload releases/idling-roi-tool.zip -> OK -> Save -> Refresh")
    print("  -> Find under Reports -> Idling ROI Tool")


if __name__ == "__main__":
    main()
