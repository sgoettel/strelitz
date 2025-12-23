#!/usr/bin/env python3
import copy
import json
import re
from pathlib import Path
from typing import Dict, List

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
    for lb in clone.findall(".//lb"):
        lb.tag = "br"
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


def derive_entry_id(item, warnings: List[str], fallback_index: int) -> str:
    label_texts = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}label")]
    for label in label_texts:
        match = re.search(r"no\s*([0-9]+)", label, flags=re.IGNORECASE)
        if match:
            return match.group(1)
        match = re.search(r"([0-9]+)", label)
        if match:
            return match.group(1)
    xml_id = item.get(XML_ID)
    if xml_id:
        warnings.append("ID aus xml:id übernommen")
        return xml_id
    warnings.append("Konnte keine Nummer finden, benutze laufende Nummer")
    return f"entry-{fallback_index}"


def parse_item(item, last_page: str, index: int) -> Dict:
    warnings: List[str] = []
    page_no = None
    if last_page and re.fullmatch(r"\d+", last_page):
        page_no = int(last_page)
    else:
        warnings.append("Keine Seitenmarke vor diesem Eintrag gefunden")

    entry_id = derive_entry_id(item, warnings, index)

    names = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}persName")]
    dates = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}date")]
    places = [normalize_text("".join(el.itertext())) for el in item.findall(f".//{{{NS}}}placeName")]

    return {
        "id": entry_id,
        "page_no": page_no,
        "text_plain": extract_plain_text(item),
        "text_html": extract_text_html(item),
        "names": dedupe(names),
        "dates": dedupe(dates),
        "places": dedupe(places),
        "warnings": warnings,
    }


def extract_entries_from_file(path: Path) -> List[Dict]:
    parser = etree.XMLParser() if HAS_LXML else None
    tree = etree.parse(str(path), parser=parser) if parser else etree.parse(str(path))
    entries: List[Dict] = []
    last_page = None
    for node in tree.getroot().iter():
        if node.tag == f"{{{NS}}}pb":
            last_page = node.get("n")
        elif node.tag == f"{{{NS}}}item":
            entries.append(parse_item(node, last_page, len(entries) + 1))
    return entries


def main():
    all_entries: List[Dict] = []
    for xml_file in sorted(TEI_DIR.glob("*.xml")):
        all_entries.extend(extract_entries_from_file(xml_file))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(all_entries)} entries to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
