#!/usr/bin/env python3
"""Inspect, never modify, a transparent portrait. Does not assess likeness."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

def inspect(path):
    path = Path(path)
    with Image.open(path) as image:
        image.load()
        if image.format != "PNG" or image.mode != "RGBA":
            raise ValueError("Require a PNG master in RGBA mode")
        if image.width != image.height or image.width < 512:
            raise ValueError("Require square canvas of at least 512 px")
        alpha = image.getchannel("A")
        if alpha.getextrema()[0] != 0 or alpha.getextrema()[1] == 0:
            raise ValueError("Require actual transparency and visible subject")
        bounds = alpha.point(lambda a: 255 if a > 16 else 0).getbbox()
        left, top, right, bottom = bounds
        margins = [left/image.width, top/image.height,
                   (image.width-right)/image.width, (image.height-bottom)/image.height]
        return {"width": image.width, "height": image.height,
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "margins_ltrb": margins,
                "warnings": ["Less than 8% safety margin: inspect framing"] if min(margins) < .08 else [],
                "likeness_review": "Requires visual comparison and real approval"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("image")
    args = parser.parse_args()
    print(json.dumps(inspect(args.image), indent=2))
