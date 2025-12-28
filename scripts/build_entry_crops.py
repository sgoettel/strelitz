#!/usr/bin/env python3
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from PIL import Image

try:
    from lxml import etree  # type: ignore
    HAS_LXML = True
except ModuleNotFoundError:  # pragma: no cover - fallback for restricted environments
    import xml.etree.ElementTree as etree  # type: ignore
    HAS_LXML = False


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "friedhofsregister_der_juedischen_gemeinde_strelitz"
ALTO_DIR = DATA_DIR / "alto"
JPG_DIR = DATA_DIR / "jpg"
ENTRIES_FILE = ROOT / "site" / "_data" / "entries.json"
OUTPUT_FILE = ROOT / "site" / "_data" / "entryCrops.json"
MANIFEST_FILE = ROOT / "site" / "_data" / "scan-manifest.json"
OUTPUT_DIR = ROOT / "site" / "assets" / "generated" / "entry-crops"

MIN_SCORE = 80
HEIGHT_RATIO_RANGE = (0.03, 0.6)


@dataclass
class TextBlock:
    hpos: float
    vpos: float
    width: float
    height: float
    lines: List[str]
    text: str


def parse_float(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_polygon_bbox(points: str) -> Optional[Tuple[float, float, float, float]]:
    coords = []
    for pair in points.split():
        if "," not in pair:
            continue
        x_str, y_str = pair.split(",", 1)
        try:
            x_val = float(x_str)
            y_val = float(y_str)
        except ValueError:
            continue
        coords.append((x_val, y_val))
    if not coords:
        return None
    xs = [x for x, _ in coords]
    ys = [y for _, y in coords]
    return (min(xs), min(ys), max(xs), max(ys))


def local_name(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def iter_by_name(node, name: str) -> Iterable:
    for elem in node.iter():
        if isinstance(elem.tag, str) and local_name(elem.tag) == name:
            yield elem


def find_first(node, name: str):
    for elem in iter_by_name(node, name):
        return elem
    return None


def parse_text_blocks(alto_path: Path) -> Tuple[Tuple[float, float], List[TextBlock]]:
    parser = etree.XMLParser() if HAS_LXML else None
    tree = etree.parse(str(alto_path), parser=parser) if parser else etree.parse(str(alto_path))
    root = tree.getroot()
    page = find_first(root, "Page")
    if page is None:
        raise ValueError(f"Page element not found in {alto_path}")
    page_width = parse_float(page.get("WIDTH"))
    page_height = parse_float(page.get("HEIGHT"))
    if page_width is None or page_height is None:
        raise ValueError(f"Missing Page WIDTH/HEIGHT in {alto_path}")

    blocks: List[TextBlock] = []
    for block in iter_by_name(page, "TextBlock"):
        hpos = parse_float(block.get("HPOS"))
        vpos = parse_float(block.get("VPOS"))
        width = parse_float(block.get("WIDTH"))
        height = parse_float(block.get("HEIGHT"))
        if None in (hpos, vpos, width, height):
            polygon = find_first(block, "Polygon")
            if polygon is not None and polygon.get("POINTS"):
                bbox = parse_polygon_bbox(polygon.get("POINTS"))
                if bbox:
                    hpos, vpos, max_x, max_y = bbox
                    width = max_x - hpos
                    height = max_y - vpos
        if None in (hpos, vpos, width, height):
            continue

        lines: List[str] = []
        for line in iter_by_name(block, "TextLine"):
            contents = [
                string.get("CONTENT", "").strip()
                for string in iter_by_name(line, "String")
                if string.get("CONTENT")
            ]
            line_text = " ".join(contents).strip()
            lines.append(line_text)
        text = " ".join([line for line in lines if line]).strip()
        blocks.append(TextBlock(hpos=hpos, vpos=vpos, width=width, height=height, lines=lines, text=text))

    return (page_width, page_height), blocks


def compile_number_patterns(entry_no: int) -> Dict[str, re.Pattern]:
    number = re.escape(str(entry_no))
    number_pattern = re.compile(rf"(?<!\d){number}(?:\.(?!\d))?", flags=re.IGNORECASE)
    prefix_pattern = re.compile(
        rf"\b(?:no|n0|nr)\b\.?\s*(?<!\d){number}(?:\.(?!\d))?",
        flags=re.IGNORECASE
    )
    return {"number": number_pattern, "prefix": prefix_pattern}


def score_block(block: TextBlock, patterns: Dict[str, re.Pattern], page_height: float) -> Optional[int]:
    if not block.text:
        return None
    if not patterns["number"].search(block.text):
        return None
    score = 10
    if patterns["prefix"].search(block.text):
        score += 100
    for idx, line in enumerate(block.lines[:2]):
        if patterns["number"].search(line):
            score += 50
            break
    height_ratio = block.height / page_height if page_height else 0
    if HEIGHT_RATIO_RANGE[0] <= height_ratio <= HEIGHT_RATIO_RANGE[1]:
        score += 10
    return score


def select_best_block(blocks: List[TextBlock], entry_no: int, page_height: float) -> Optional[TextBlock]:
    patterns = compile_number_patterns(entry_no)
    scored: List[Tuple[int, TextBlock]] = []
    for block in blocks:
        score = score_block(block, patterns, page_height)
        if score is None:
            continue
        scored.append((score, block))
    if not scored:
        return None
    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_block = scored[0]
    if best_score < MIN_SCORE:
        return None
    return best_block


def compute_crop_box(block: TextBlock, page_size: Tuple[float, float], image_size: Tuple[int, int]) -> Tuple[int, int, int, int]:
    page_width, page_height = page_size
    img_width, img_height = image_size
    sx = img_width / page_width
    sy = img_height / page_height
    x1 = block.hpos * sx
    y1 = block.vpos * sy
    x2 = (block.hpos + block.width) * sx
    y2 = (block.vpos + block.height) * sy

    pad = max(20, int(round(img_width * 0.01)))
    x1 = max(0, math.floor(x1 - pad))
    y1 = max(0, math.floor(y1 - pad))
    x2 = min(img_width, math.ceil(x2 + pad))
    y2 = min(img_height, math.ceil(y2 + pad))
    return x1, y1, x2, y2


def load_manifest() -> Dict:
    if not MANIFEST_FILE.exists():
        raise FileNotFoundError(f"Scan manifest not found: {MANIFEST_FILE}")
    return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))


def resolve_image_basename(manifest: Dict, page_no: int) -> Optional[str]:
    entry = manifest.get("byPb", {}).get(str(page_no))
    if not entry:
        return None
    image_url = entry.get("image")
    if not image_url:
        return None
    return Path(image_url).name


def main() -> None:
    if not ENTRIES_FILE.exists():
        raise FileNotFoundError(f"Entries file not found: {ENTRIES_FILE}")
    manifest = load_manifest()
    entries = json.loads(ENTRIES_FILE.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("entries.json must contain a list of entries")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    crop_map: Dict[str, str] = {}
    unmatched: List[str] = []

    for entry in entries:
        entry_no = entry.get("no")
        page_no = entry.get("page_no")
        slug = entry.get("slug")
        if not slug or entry_no is None or page_no is None:
            continue

        if isinstance(entry_no, int):
            entry_number = entry_no
        elif isinstance(entry_no, str):
            match = re.search(r"\d+", entry_no)
            if not match:
                continue
            entry_number = int(match.group(0))
        else:
            continue

        basename = resolve_image_basename(manifest, page_no)
        if not basename:
            unmatched.append(f"{slug} (no={entry_no}, page_no={page_no}, image=missing)")
            continue

        alto_path = ALTO_DIR / Path(basename).with_suffix(".xml")
        jpg_path = JPG_DIR / basename
        if not alto_path.exists() or not jpg_path.exists():
            unmatched.append(f"{slug} (no={entry_no}, page_no={page_no}, image={basename})")
            continue

        try:
            page_size, blocks = parse_text_blocks(alto_path)
        except Exception as exc:
            unmatched.append(f"{slug} (no={entry_no}, page_no={page_no}, image={basename}, error={exc})")
            continue

        best_block = select_best_block(blocks, entry_number, page_size[1])
        if not best_block:
            unmatched.append(f"{slug} (no={entry_no}, page_no={page_no}, image={basename})")
            continue

        with Image.open(jpg_path) as img:
            crop_box = compute_crop_box(best_block, page_size, img.size)
            if crop_box[2] <= crop_box[0] or crop_box[3] <= crop_box[1]:
                unmatched.append(f"{slug} (no={entry_no}, page_no={page_no}, image={basename}, error=invalid-crop)")
                continue
            cropped = img.crop(crop_box)
            output_path = OUTPUT_DIR / f"{slug}.jpg"
            cropped.save(output_path, format="JPEG", quality=85, optimize=True)

        crop_url = f"/assets/generated/entry-crops/{slug}.jpg"
        crop_map[slug] = crop_url

    OUTPUT_FILE.write_text(json.dumps(crop_map, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[entry-crops] Wrote {len(crop_map)} crop URLs to {OUTPUT_FILE}")

    if unmatched:
        print("[entry-crops] Unmatched entries (fallback to full-page thumbnail):")
        for item in unmatched:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
