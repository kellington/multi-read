#!/usr/bin/env python3
import argparse
import html
import json
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path

from vocabulary import (
    analyze_volume,
    build_records,
    chapter_tokens,
    chapter_sources,
    difficulty_map,
    enrich_glossary,
    load_flelex,
    load_lexique,
    load_nlp,
    loose_fold,
)


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
    "dantès": ("Edmond Dantès", "The young sailor serving aboard the Pharaon."),
    "edmond": ("Edmond Dantès", "The young sailor at the center of the story."),
    "morrel": ("Morrel", "The shipowner who trusts Dantès."),
    "danglars": ("Danglars", "The ship's accountant, uneasy about Dantès."),
    "leclère": ("Captain Leclère", "The Pharaon's captain, whose death is reported in this chapter."),
    "marseille": ("Marseille", "The French port where the Pharaon returns."),
    "capitaine": ("captain", "The commander of a ship."),
    "équipage": ("crew", "The people working on a ship."),
    "empereur": ("emperor", "In this story, Napoleon."),
    "lettre": ("letter", "Letters and messages drive several later plot turns."),
    "espérance": ("hope", "Here, Dantès's hope of becoming captain."),
    "pavillon": ("flag", "The ship's flag is lowered to mark mourning."),
    "douaniers": ("customs officers", "Officials checking the ship's cargo and papers."),
    "besogne": ("work, task", "A familiar word for work; here, part of a decision has been made."),
    "tristesse": ("sadness", "The mood on board after the captain's death."),
    "résolution": ("determination", "Dantès's calm resolve in the face of danger."),
    "interlocuteur": ("person being spoken to", "The person in the conversation with Dantès."),
    "rames": ("oars", "The blades used to propel the small boat."),
}

PLAIN_REPLACEMENTS = (
    (r"\bla vigie\b", "le guetteur"),
    (r"\ble trois-màts le Pharaon\b", "le navire Pharaon à trois mâts"),
    (r"\bses trois huniers\b", "ses trois voiles hautes"),
    (r"\bson grand foc\b", "sa grande voile avant"),
    (r"\bsa brigantine\b", "sa voile arrière"),
    (r"\bses haubans de beaupré décrochés\b", "ses cordages à l'avant du navire détachés"),
    (r"\bune fièvre cérébrale\b", "une grave fièvre"),
    (r"\bson ancre était au mouillage\b", "son ancre était prête"),
    (r"\bau mouillage\b", "à l'ancrage"),
    (r"\ble mouillage\b", "l'ancrage"),
    (r"\bson mouillage\b", "son ancrage"),
    (r"\bne point escompter pour 25, 000 francs\b", "ne pas compter sur 25 000 francs"),
    (r"\bobséquieux envers\b", "flatteur envers"),
    (r"\bles écoutes\b", "les cordages des voiles"),
    (r"\baux drisses\b", "aux cordages qui hissent les voiles"),
    (r"\baux cargues des voiles\b", "aux cordages qui replient les voiles"),
    (r"\ble foc et la brigantine\b", "la voile avant et la voile arrière"),
)

GLOSSARY_FORMS = {
    "trois-mats": ["trois-màts"],
    "pilote-cotier": ["pilote côtier"],
    "chateau-d-if": ["château d’If", "château d'If"],
    "ecoutes": ["écoutes"],
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
    parts = re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ý—])", paragraph)
    sentences = [part.strip() for part in parts if part.strip()]
    return sentences or [paragraph]


def plain_units(paragraph):
    text = paragraph
    for pattern, replacement in PLAIN_REPLACEMENTS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    if not text.startswith("—") and "—" not in text:
        text = re.sub(
            r";\s+((?:il|elle|ils|elles|je|nous|vous|tu|le|la|les|un|une|ce|cette|son|sa|ses)\b)",
            lambda match: ". " + match.group(1).capitalize(), text, flags=re.IGNORECASE,
        )
    text = re.sub(r"\s+", " ", text)
    return [unit[0].upper() + unit[1:] for unit in split_sentences(text)]


def glossary_keys_for(text, entries=None):
    lower = loose_fold(text)
    keys = []
    for key, entry in (entries or GLOSSARY).items():
        forms = [key] if isinstance(entry, tuple) else [entry["headword"], *(entry.get("forms") or [])]
        for form in forms:
            pattern = r"(?<!\w)" + re.escape(loose_fold(form)) + r"(?!\w)"
            if re.search(pattern, lower):
                keys.append(slug(key))
                break
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


def build_chapter(epub, chapter_path, chapter_id, chapter_number, title, records, volume_chapters, source_info):
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
            "sourceNote": "Generated from EPUB chapter HTML. Plain has first-pass vocabulary-guided substitutions and segmentation; it still needs reading review.",
            "glossaryKeys": glossary_keys_for(paragraph),
            "representations": {
                "plain": {
                    "label": "Plain",
                    "level": "First-pass bridge",
                    "description": "Some specialized words use simpler French. The story stays close to the original.",
                    "sentences": sentence_objects(plain, f"{passage_id}-plain", "vocabulary-aware-first-pass"),
                },
                "guided": {
                    "label": "Guided",
                    "level": "B1/B2",
                    "description": "Dumas's original French, with help on selected words.",
                    "sentences": sentence_objects(original, f"{passage_id}-guided", "original"),
                },
                "original": {
                    "label": "Original",
                    "level": "B2/C1",
                    "description": "Dumas's original French, without word highlighting.",
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

    chapter_text = " ".join(parser.paragraphs)
    later_text = " ".join(
        paragraph
        for number, _, paragraphs in volume_chapters
        if number > chapter_number
        for paragraph in paragraphs
    )
    enrich_glossary(glossary, records, chapter_text, later_text)
    for key, forms in GLOSSARY_FORMS.items():
        glossary[key]["forms"] = forms if key == "ecoutes" else list(dict.fromkeys(glossary[key]["forms"] + forms))
    for passage in passages:
        source_text = " ".join(passage["originalComparison"])
        passage["glossaryKeys"] = glossary_keys_for(source_text, glossary)
        passage["vocabularyKeys"] = passage["glossaryKeys"]

    return {
        "schemaVersion": 2,
        "bookId": "monte-cristo",
        "chapterId": chapter_id,
        "chapterNumber": chapter_number,
        "title": title,
        "status": "vocabulary-baseline-first-pass",
        "nextChapterId": f"c{chapter_number + 1:02d}",
        "source": {
            "epub": str(epub),
            "file": chapter_path,
            "paragraphCount": len(parser.paragraphs),
        },
        "processingNotes": [
            "Original and guided retain the EPUB source text.",
            "Plain uses reviewed first-pass substitutions for selected low-value nautical terms and still needs reading feedback.",
            "Vocabulary decisions use recurrence in the 55-chapter available volume, not the complete novel.",
            "CEFR and modern frequency are included only when their source tables supplied a match; missing values are not guessed.",
            "Sentence translations are still blank; their scope will be decided after a fresh reading pass.",
        ],
        "vocabularyAnalysis": source_info,
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
    parser.add_argument("--flelex", type=Path, help="Local FLELex TSV/CSV source (optional)")
    parser.add_argument("--lexique", type=Path, help="Local Lexique TSV/CSV source (optional)")
    parser.add_argument("--out-vocabulary", type=Path, help="Defaults beside --out-json")
    parser.add_argument("--out-difficulty-map", type=Path, help="Defaults beside --out-json")
    parser.add_argument("--out-tokens", type=Path, help="Defaults beside --out-json")
    args = parser.parse_args()

    chapter_number = int(args.chapter_id.removeprefix("c"))
    volume_chapters = chapter_sources(Path(args.epub), ChapterParser)
    nlp = load_nlp()
    counts, forms, token_count = analyze_volume(volume_chapters, nlp)
    flelex = load_flelex(args.flelex)
    lexique = load_lexique(args.lexique)
    records = build_records(volume_chapters, counts, forms, flelex, lexique, chapter_number)
    chapter_paragraphs = next(paragraphs for number, _, paragraphs in volume_chapters if number == chapter_number)
    tokens = chapter_tokens(chapter_paragraphs, args.chapter_id, nlp)
    source_info = {
        "volumeChapters": len(volume_chapters),
        "analyzedContentTokens": token_count,
        "tokenizer": "spaCy fr_core_news_sm",
        "flelex": args.flelex.name if args.flelex else None,
        "lexique": args.lexique.name if args.lexique else None,
        "vocabularyFile": f"{args.chapter_id}.vocabulary.json",
        "difficultyMapFile": f"{args.chapter_id}.difficulty-map.json",
        "tokensFile": f"{args.chapter_id}.tokens.json",
    }
    chapter = build_chapter(Path(args.epub), args.chapter_path, args.chapter_id, chapter_number, args.title, records, volume_chapters, source_info)
    out_json = Path(args.out_json)
    out_js = Path(args.out_js)
    out_vocabulary = args.out_vocabulary or out_json.with_name(f"{args.chapter_id}.vocabulary.json")
    out_difficulty_map = args.out_difficulty_map or out_json.with_name(f"{args.chapter_id}.difficulty-map.json")
    out_tokens = args.out_tokens or out_json.with_name(f"{args.chapter_id}.tokens.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_js.parent.mkdir(parents=True, exist_ok=True)
    out_vocabulary.parent.mkdir(parents=True, exist_ok=True)
    out_difficulty_map.parent.mkdir(parents=True, exist_ok=True)
    out_tokens.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_js.write_text("window.MultiReadChapter = " + json.dumps(chapter, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    out_vocabulary.write_text(json.dumps({"source": source_info, "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_difficulty_map.write_text(json.dumps(difficulty_map(records), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out_tokens.write_text(json.dumps({"chapterId": args.chapter_id, "tokens": tokens}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
