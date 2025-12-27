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
    allowed_tags = {"p", "br", "span", "time", "ol", "ul", "li", "del"}

    def add_class(elem, class_name: str) -> None:
        classes = elem.get("class", "").split()
        if class_name not in classes:
            classes.append(class_name)
        if classes:
            elem.set("class", " ".join(classes))
    for elem in clone.iter():
        if not isinstance(elem.tag, str):
            continue
        if elem.tag == "lb":
            elem.tag = "br"
        elif elem.tag == "del":
            add_class(elem, "tei-del")
        elif elem.tag == "label":
            elem.tag = "span"
            add_class(elem, "tei-label")
        elif elem.tag == "fw":
            elem.tag = "span"
            add_class(elem, "tei-fw")
        elif elem.tag == "persName":
            elem.tag = "span"
            add_class(elem, "tei-persname")
        elif elem.tag == "date":
            elem.tag = "time"
            add_class(elem, "tei-date")
        elif elem.tag == "placeName":
            elem.tag = "span"
            add_class(elem, "tei-placename")
        elif elem.tag == "roleName":
            elem.tag = "span"
            add_class(elem, "tei-rolename")
        elif elem.tag == "unclear":
            elem.tag = "span"
            add_class(elem, "tei-unclear")
        elif elem.tag == "list":
            rend = (elem.get("rend") or "").lower()
            elem.tag = "ol" if "numbered" in rend else "ul"
        elif elem.tag == "item":
            elem.tag = "li"
        elif elem.tag == "foreign":
            elem.tag = "span"
            add_class(elem, "tei-foreign")
            lang = (elem.get("lang") or "").lower()
            if lang:
                elem.set("lang", lang)
            if lang in {"hbo", "heb", "he"}:
                add_class(elem, "tei-foreign-hbo")

    def remove_child_preserve_tail(parent, child, index: int) -> None:
        tail = child.tail
        parent.remove(child)
        if tail:
            if index == 0:
                parent.text = (parent.text or "") + tail
            else:
                sibling = parent[index - 1]
                sibling.tail = (sibling.tail or "") + tail

    def cleanup_breaks(parent) -> None:
        while len(parent) > 0 and parent[0].tag == "br":
            remove_child_preserve_tail(parent, parent[0], 0)
        i = 0
        consecutive = 0
        while i < len(parent):
            child = parent[i]
            if child.tag == "br":
                consecutive += 1
                if consecutive > 2:
                    remove_child_preserve_tail(parent, child, i)
                    continue
            else:
                consecutive = 0
            i += 1

    if HAS_LXML:
        present_tags = {
            elem.tag
            for elem in clone.iter()
            if isinstance(elem.tag, str)
        }
        disallowed_tags = present_tags - allowed_tags
        if disallowed_tags:
            etree.strip_tags(clone, *sorted(disallowed_tags))
    else:  # pragma: no cover - fallback for restricted environments
        def unwrap(parent, elem):
            index = list(parent).index(elem)
            if elem.text:
                if index == 0:
                    parent.text = (parent.text or "") + elem.text
                else:
                    sibling = parent[index - 1]
                    sibling.tail = (sibling.tail or "") + elem.text
            children = list(elem)
            for child in children:
                parent.insert(index, child)
                index += 1
            tail = elem.tail
            parent.remove(elem)
            if tail:
                if index == 0:
                    parent.text = (parent.text or "") + tail
                else:
                    sibling = parent[index - 1]
                    sibling.tail = (sibling.tail or "") + tail
        for parent in clone.iter():
            for child in list(parent):
                if not isinstance(child.tag, str):
                    continue
                if child.tag not in allowed_tags:
                    unwrap(parent, child)

    cleanup_breaks(clone)
    for paragraph in clone.iter("p"):
        cleanup_breaks(paragraph)
    html_parts: List[str] = []
    for child in clone:
        html_parts.append(etree.tostring(child, encoding="unicode", method="html"))
    if not html_parts:
        return "".join(clone.itertext())
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
