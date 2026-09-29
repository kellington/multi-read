#!/usr/bin/env python3
import argparse
import html
import json
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path


GLOSSARY = {
    "vigie": ("lookout; watch post", "Can mean the watcher or the lookout position."),
    "trois-mats": ("three-masted ship", "A sailing vessel with three masts."),
    "pharaon": ("the ship's name", "Dantes is second mate on this vessel."),
    "smyrne": ("Smyrna, now Izmir in Turkey", "One of the Pharaon's eastern Mediterranean ports."),
    "trieste": ("a port city on the Adriatic", "Another stop on the Pharaon's route."),
    "naples": ("Naples", "The last named port before Marseille."),
    "pilote cotier": ("coastal pilot", "A local specialist who guides ships through harbor waters."),
    "aussitot": ("immediately, at once", "Often marks quick action in narration."),
    "chateau d'if": ("fortress on an island off Marseille", "This place becomes important later in the novel."),
    "navire": ("ship, vessel", "A more formal word than bateau."),
    "batiment": ("vessel, ship", "In this chapter it is nautical, not a building."),
    "armateur": ("shipowner", "A person or company that equips and operates merchant ships."),
    "curieux": ("curious onlookers", "As a noun here, people who gather to watch."),
    "mouillage": ("anchoring; anchorage", "The act or place of anchoring a ship."),
    "haubans": ("stays, rigging cables", "Cables that support a mast."),
    "beaupre": ("bowsprit", "A spar projecting from the front of a sailing ship."),
    "huniers": ("topsails", "Sails set above the lower sails."),
    "foc": ("jib", "A triangular sail near the front of a ship."),
    "brigantine": ("spanker sail", "A fore-and-aft sail on the after mast."),
    "allure": ("bearing, pace, manner of moving", "Here it describes the ship's slow, sad entrance."),
    "bord": ("on board", "A bord means aboard a ship."),
    "barque": ("small boat", "A small craft used in the harbor."),
    "anse": ("cove, small bay", "A coastal indentation."),
    "muraille": ("side, wall", "Here, the side of the ship."),
    "chargement": ("cargo", "The goods carried by the ship."),
    "cargaison": ("cargo", "The load of goods on a vessel."),
    "fièvre cérébrale": ("brain fever", "An older expression for a severe fever affecting the brain."),
    "matelots": ("sailors", "Members of the ship's crew."),
    "ecoutes": ("sheets", "Ropes used to control sails."),
    "drisses": ("halyards", "Ropes used to raise sails."),
    "cargues": ("clewlines or brails", "Ropes used to gather in sails."),
    "hamac": ("hammock", "Used here in the burial at sea description."),
    "boulet": ("cannonball", "Used as a weight in the burial at sea."),
    "escompter": ("to discount; to reckon on", "Here, to count a voyage's profit in advance."),
    "comptable": ("accountant, purser", "Danglars's role aboard the Pharaon."),
    "obséquieux": ("obsequious", "Overly deferential to superiors."),
    "subordonnés": ("subordinates", "People lower in rank."),
    "relâche": ("stopover", "A pause in a voyage."),
    "douane": ("customs", "Officials who inspect goods entering port."),
    "consigne": ("port authority office", "Here, harbor administration."),
    "canebière": ("La Canebiere", "A famous street in Marseille."),
}


class ChapterParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_p = False
        self.current = []
        self.paragraphs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "p" and attrs.get("class") == "p-indent":
            self.in_p = True
            self.current = []

    def handle_endtag(self, tag):
        if tag == "p" and self.in_p:
            text = normalize_text("".join(self.current))
            if text:
                self.paragraphs.append(text)
            self.in_p = False
            self.current = []

    def handle_data(self, data):
        if self.in_p:
            self.current.append(data)


def normalize_text(value):
    value = html.unescape(value)
    value = value.replace("\u00a0", " ")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s+([,.;:!?])", r"\1", value)
    value = value.strip()
    value = re.sub(r"^LE\b", "Le", value)
    value = value.replace("LE 24 février 1815", "Le 24 février 1815")
    return value


def split_sentences(paragraph):
    if paragraph.startswith("—"):
        return [paragraph]
    parts = re.split(r"(?<=[.!?])\s+", paragraph)
    sentences = [part.strip() for part in parts if part.strip()]
    return sentences or [paragraph]


def plain_units(paragraph):
    text = paragraph
    text = re.sub(r"\s*;\s*", ". ", text)
    text = re.sub(r",\s+(?=(?:mais|car|et|puis|quoique|tandis que|de sorte que)\b)", ". ", text)
    text = re.sub(r"\s+", " ", text)
    return split_sentences(text)


def glossary_keys_for(text):
    lower = text.lower()
    keys = []
    for key in GLOSSARY:
        if key in lower:
            keys.append(slug(key))
    return keys


def slug(value):
    value = value.lower()
    value = value.replace("è", "e").replace("é", "e").replace("ê", "e")
    value = value.replace("à", "a").replace("â", "a")
    value = value.replace("î", "i").replace("ï", "i")
    value = value.replace("ô", "o")
    value = value.replace("ù", "u").replace("û", "u")
    value = value.replace("ç", "c")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def sentence_objects(passages, prefix, source=""):
    return [
        {
            "id": f"{prefix}-s{index + 1:02d}",
            "text": sentence,
            "translation": "",
            "source": source,
        }
        for index, sentence in enumerate(passages)
    ]


def build_chapter(epub, chapter_path, chapter_id, title):
    with zipfile.ZipFile(epub) as archive:
        source_html = archive.read(chapter_path).decode("utf-8")

    parser = ChapterParser()
    parser.feed(source_html)

    passages = []
    for index, paragraph in enumerate(parser.paragraphs, start=1):
        passage_id = f"{chapter_id}-p{index:03d}"
        plain = plain_units(paragraph)
        original = split_sentences(paragraph)
        passages.append({
            "id": passage_id,
            "sequence": index,
            "title": title,
            "book": "Le Comte de Monte-Cristo",
            "author": "Alexandre Dumas",
            "sourceEpub": str(epub),
            "sourceChapter": chapter_path,
            "sourceParagraph": index,
            "sourceNote": "Generated from EPUB chapter HTML. Plain is a mechanical first-pass segmentation, not a reviewed simplification.",
            "glossaryKeys": glossary_keys_for(paragraph),
            "representations": {
                "plain": {
                    "label": "Plain",
                    "level": "A2/B1 bridge",
                    "description": "Mechanical first pass: long source sentences are broken into smaller reading units.",
                    "sentences": sentence_objects(plain, f"{passage_id}-plain", "mechanical-segmentation"),
                },
                "guided": {
                    "label": "Guided",
                    "level": "B1/B2",
                    "description": "Original text with glossary highlighting and sentence support hooks.",
                    "sentences": sentence_objects(original, f"{passage_id}-guided", "original"),
                },
                "original": {
                    "label": "Original",
                    "level": "B2/C1",
                    "description": "Original paragraph from the EPUB, normalized for browser display.",
                    "sentences": sentence_objects(original, f"{passage_id}-original", "original"),
                },
            },
            "originalComparison": original,
        })

    glossary = {}
    for key, (meaning, note) in GLOSSARY.items():
        glossary[slug(key)] = {
            "headword": key,
            "meaning": meaning,
            "note": note,
        }

    return {
        "schemaVersion": 1,
        "bookId": "monte-cristo",
        "chapterId": chapter_id,
        "chapterNumber": 1,
        "title": title,
        "status": "processed-first-pass",
        "nextChapterId": "c02",
        "source": {
            "epub": str(epub),
            "file": chapter_path,
            "paragraphCount": len(parser.paragraphs),
        },
        "processingNotes": [
            "Original and guided retain the EPUB source text.",
            "Plain is mechanically segmented and should be improved after reading feedback.",
            "Sentence translations are intentionally blank in schema v1; add them if feedback says they are essential.",
        ],
        "passages": passages,
        "glossary": glossary,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epub", required=True)
    parser.add_argument("--chapter-path", required=True)
    parser.add_argument("--chapter-id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--out-json", required=True)
    parser.add_argument("--out-js", required=True)
    args = parser.parse_args()

    chapter = build_chapter(Path(args.epub), args.chapter_path, args.chapter_id, args.title)
    out_json = Path(args.out_json)
    out_js = Path(args.out_js)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_js.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_js.write_text("window.MultiReadChapter = " + json.dumps(chapter, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")


if __name__ == "__main__":
    main()
