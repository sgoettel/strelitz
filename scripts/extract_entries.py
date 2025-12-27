#!/usr/bin/env python3
import copy
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple


seen_ids = {}
def uniq(base: str) -> str:
    base = str(base)
    n = seen_ids.get(base, 0) + 1
    seen_ids[base] = n
    return base if n == 1 else f"{base}-{n}"

try:
    from lxml import etree  # type: ignore
    HAS_LXML = True
except ModuleNotFoundError:  # pragma: no cover - fallback for restricted environments
    import xml.etree.ElementTree as etree  # type: ignore
    HAS_LXML = False

NS = "http://www.tei-c.org/ns/1.0"
XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
ROOT = Path(__file__).resolve().parent.parent
TEI_DIR = ROOT / "friedhofsregister_der_juedischen_gemeinde_strelitz" / "TEI"
OUTPUT_FILE = ROOT / "site" / "_data" / "entries.json"
PAGES_FILE = ROOT / "site" / "_data" / "pages.json"


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def strip_namespaces(el):
    for elem in el.iter():
        if not isinstance(elem.tag, str):
            continue
        if "}" in elem.tag:
            elem.tag = elem.tag.split("}", 1)[1]
        for attr_name in list(elem.attrib):
            if "}" in attr_name:
                elem.attrib[attr_name.split("}", 1)[1]] = elem.attrib.pop(attr_name)


def extract_text_html(item) -> str:
    clone = copy.deepcopy(item)
    strip_namespaces(clone)
    allowed_tags = {"br", "del", "span", "time", "ol", "ul", "li"}
    for elem in clone.iter():
        if not isinstance(elem.tag, str):
            continue
        if elem.tag == "lb":
            elem.tag = "br"
        elif elem.tag == "del":
            elem.set("class", f"{elem.get('class', '')} tei-del".strip())
        elif elem.tag == "persName":
            elem.tag = "span"
            elem.set("class", f"{elem.get('class', '')} tei-persname".strip())
        elif elem.tag == "date":
            elem.tag = "time"
            elem.set("class", f"{elem.get('class', '')} tei-date".strip())
        elif elem.tag == "foreign":
            elem.tag = "span"
            elem.set("class", f"{elem.get('class', '')} tei-foreign".strip())
            lang = (elem.get("lang") or "").lower()
            if lang:
                elem.set("lang", lang)
            if lang.startswith("he") or lang.startswith("yi") or lang.startswith("heb"):
                elem.set("dir", "rtl")

    def unwrap_disallowed(parent):
        i = 0
        while i < len(parent):
            child = parent[i]
            unwrap_disallowed(child)
            if isinstance(child.tag, str) and child.tag in allowed_tags:
                i += 1
                continue
            inserted = list(child)
            if child.text:
                if i == 0:
                    parent.text = (parent.text or "") + child.text
                else:
                    prev = parent[i - 1]
                    prev.tail = (prev.tail or "") + child.text
            insert_pos = i
            for grandchild in inserted:
                child.remove(grandchild)
                parent.insert(insert_pos, grandchild)
                insert_pos += 1
            tail_text = child.tail or ""
            parent.remove(child)
            if tail_text:
                if insert_pos == 0:
                    parent.text = (parent.text or "") + tail_text
                else:
                    prev = parent[insert_pos - 1]
                    prev.tail = (prev.tail or "") + tail_text
            if inserted:
                i += len(inserted)

    unwrap_disallowed(clone)
    html_parts: List[str] = []
    for child in clone:
        html_parts.append(etree.tostring(child, encoding="unicode", method="html"))
    if not html_parts:
        html_parts.append(etree.tostring(clone, encoding="unicode", method="html"))
    return "".join(html_parts)


def extract_plain_text(item) -> str:
    return normalize_text("".join(item.itertext()))


def dedupe(values: List[str]) -> List[str]:
    seen = set()
    result = []
    for val in values:
        if not val:
            continue
        if val in seen:
            continue
        seen.add(val)
        result.append(val)
    return result


def derive_entry_no(item, warnings: List[str]):
    label_texts = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}label")]
    for label in label_texts:
        m = re.search(r"no\s*([0-9]+)", label, flags=re.IGNORECASE)
        if m:
            return int(m.group(1))
        m = re.search(r"\b([0-9]+)\b", label)
        if m:
            return int(m.group(1))
    warnings.append("Konnte keine Eintragsnummer im Label finden")
    return None



def parse_item(item, last_page: str, index: int) -> Dict:
    warnings: List[str] = []
    page_no = None
    if last_page and re.fullmatch(r"\d+", last_page):
        page_no = int(last_page)
    else:
        warnings.append("Keine Seitenmarke vor diesem Eintrag gefunden")

    entry_no = derive_entry_no(item, warnings)

    # stabile, eindeutige URL-ID: bevorzugt xml:id, sonst Sequenz
    base_id = item.get(XML_ID) or f"e{index:04d}"
    entry_id = uniq(base_id)


    names = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}persName")]
    dates = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}date")]
    places = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}placeName")]

    return {
        "id": entry_id,
        "no": entry_no,
        "page_no": page_no,
        "text_plain": extract_plain_text(item),
        "text_html": extract_text_html(item),
        "names": dedupe(names),
        "dates": dedupe(dates),
        "places": dedupe(places),
        "warnings": warnings,
    }


def extract_entries_from_file(path: Path) -> Tuple[List[Dict], Set[int]]:
    parser = etree.XMLParser() if HAS_LXML else None
    tree = etree.parse(str(path), parser=parser) if parser else etree.parse(str(path))
    entries: List[Dict] = []
    pages: Set[int] = set()
    last_page = None
    for node in tree.getroot().iter():
        if node.tag == f"{{{NS}}}pb":
            last_page = node.get("n")
            if last_page and re.fullmatch(r"\d+", last_page):
                pages.add(int(last_page))
        elif node.tag == f"{{{NS}}}item":
            entries.append(parse_item(node, last_page, len(entries) + 1))
    return entries, pages


def main():
    all_entries: List[Dict] = []
    all_pages: Set[int] = set()
    for xml_file in sorted(TEI_DIR.glob("*.xml")):
        entries, pages = extract_entries_from_file(xml_file)
        all_entries.extend(entries)
        all_pages.update(pages)
    id_counts = Counter(entry["id"] for entry in all_entries)
    id_seen = defaultdict(int)
    for entry in all_entries:
        entry_id = entry["id"]
        if id_counts[entry_id] > 1:
            id_seen[entry_id] += 1
            entry["slug"] = f"{entry_id}-{id_seen[entry_id]}"
            entry.setdefault("warnings", []).append("Doppelte ID, URL-Suffix ergänzt")
        else:
            entry["slug"] = str(entry_id)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(all_entries)} entries to {OUTPUT_FILE}")
    with PAGES_FILE.open("w", encoding="utf-8") as f:
        json.dump(sorted(all_pages), f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(all_pages)} pages to {PAGES_FILE}")


if __name__ == "__main__":
    main()
