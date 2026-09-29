"""Inspectable vocabulary analysis for the available French Monte-Cristo volume.

The checked-in chapter remains static. This module runs only while rebuilding it.
Optional FLELex and Lexique tables enrich the local recurrence evidence.
"""

from __future__ import annotations

import csv
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


WORD_RE = re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*", re.UNICODE)
CHAPTER_RE = re.compile(r"_c(\d+)\.html$")
NAMES = {
    "dantès", "edmond", "mercédès", "morrel", "danglars", "fernand",
    "pharaon", "marseille", "smyrne", "trieste", "naples", "leclère",
    "notre-dame-de-la-garde", "château d’if", "chateau d'if", "canebière",
}
COMMON_DISCOURSE = {"oui", "non", "monsieur", "madame"}
GLOSSARY_TREATMENT = {
    "pharaon": "ignore_or_gloss", "smyrne": "ignore_or_gloss",
    "trieste": "ignore_or_gloss", "naples": "ignore_or_gloss",
    "chateau d'if": "ignore_or_gloss", "canebière": "ignore_or_gloss",
    "trois-mats": "ignore_or_gloss", "pilote cotier": "ignore_or_gloss",
    "haubans": "simplify", "beaupre": "simplify", "huniers": "simplify",
    "foc": "simplify", "brigantine": "simplify", "ecoutes": "simplify",
    "drisses": "simplify", "cargues": "simplify", "fièvre cérébrale": "ignore_or_gloss",
}


def fold(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold().replace("’", "'").strip()


def loose_fold(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFD", fold(value))
        if unicodedata.category(char) != "Mn"
    )


def chapter_sources(epub: Path, parse_chapter) -> list[tuple[int, str, list[str]]]:
    chapters = []
    with zipfile.ZipFile(epub) as archive:
        for path in archive.namelist():
            match = CHAPTER_RE.search(path)
            if not match:
                continue
            parser = parse_chapter()
            parser.feed(archive.read(path).decode("utf-8"))
            chapters.append((int(match.group(1)), path, parser.paragraphs))
    return sorted(chapters)


def load_nlp():
    try:
        import spacy
        return spacy.load("fr_core_news_sm", disable=["parser", "ner"])
    except (ImportError, OSError) as exc:
        raise RuntimeError(
            "Vocabulary analysis needs spaCy and fr_core_news_sm. "
            "Install the documented processing dependencies before rebuilding the chapter."
        ) from exc


def analyze_volume(chapters, nlp):
    chapter_counts = defaultdict(Counter)
    forms = defaultdict(Counter)
    token_count = 0
    for number, _, paragraphs in chapters:
        for doc in nlp.pipe(paragraphs, batch_size=64):
            for token in doc:
                if not token.is_alpha or token.is_stop:
                    continue
                surface = fold(token.text)
                lemma = fold(token.lemma_ or token.text)
                pos = token.pos_ or "X"
                if surface in NAMES or lemma in NAMES:
                    lemma, pos = surface, "PROPN"
                if not lemma or len(lemma) < 2:
                    continue
                key = (lemma, pos)
                chapter_counts[number][key] += 1
                forms[key][surface] += 1
                token_count += 1
    return chapter_counts, forms, token_count


def chapter_tokens(paragraphs, chapter_id, nlp):
    rows = []
    for index, doc in enumerate(nlp.pipe(paragraphs, batch_size=64), start=1):
        passage_id = f"{chapter_id}-p{index:03d}"
        for token in doc:
            if not token.is_alpha:
                continue
            surface = fold(token.text)
            lemma = fold(token.lemma_ or token.text)
            pos = token.pos_ or "X"
            if surface in NAMES or lemma in NAMES:
                lemma, pos = surface, "PROPN"
            rows.append({
                "passageId": passage_id,
                "start": token.idx,
                "end": token.idx + len(token.text),
                "word": token.text,
                "lemma": lemma,
                "partOfSpeech": pos,
                "isStop": token.is_stop,
            })
    return rows


def read_table(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        sample = stream.read(4096)
        stream.seek(0)
        dialect = csv.Sniffer().sniff(sample, delimiters="\t,;")
        yield from csv.DictReader(stream, dialect=dialect)


def first_value(row, *names):
    lowered = {key.lower().strip(): value for key, value in row.items() if key}
    for name in names:
        value = lowered.get(name.lower())
        if value not in (None, ""):
            return value.strip()
    return None


def coarse_pos(tag):
    prefix = (tag or "").upper().split(":", 1)[0]
    return {
        "NOM": "NOUN", "VER": "VERB", "AUX": "AUX", "ADJ": "ADJ",
        "ADV": "ADV", "PRO": "PRON", "PRP": "ADP", "PRE": "ADP",
        "KON": "CCONJ", "CON": "CCONJ", "DET": "DET", "ART": "DET",
        "INT": "INTJ", "ONO": "INTJ",
    }.get(prefix)


def load_flelex(path: Path | None):
    if not path:
        return {}
    levels = {}
    for row in read_table(path):
        lemma = first_value(row, "lemma", "lemme", "word")
        level = first_value(row, "level", "cefr", "cefr_level", "niveau")
        pos = coarse_pos(first_value(row, "tag", "pos"))
        if lemma and pos and level and level.upper() in {"A1", "A2", "B1", "B2", "C1", "C2"}:
            levels.setdefault((fold(lemma), pos), level.upper())
    return levels


def load_lexique(path: Path | None):
    if not path:
        return {}
    frequencies = {}
    for row in read_table(path):
        lemma = first_value(row, "4_Lemme", "lemme", "lemma")
        pos = coarse_pos(first_value(row, "5_Cgram", "cgram", "pos"))
        value = first_value(row, "12_FreqLemme", "freqfilms2", "freqfilms", "freq", "frequency", "freqsubtlex", "freq_subtitles")
        if not lemma or not pos or not value:
            continue
        try:
            frequency = float(value.replace(",", "."))
        except ValueError:
            continue
        key = (fold(lemma), pos)
        frequencies[key] = max(frequencies.get(key, 0), frequency)
    return frequencies


def frequency_band(value):
    if value is None:
        return None
    if value >= 10:
        return "common"
    if value >= 1:
        return "mid"
    return "rare"


def classify(record):
    if record["properNoun"]:
        return "ignore_or_gloss", "Name or place; understand its role without memorizing it as vocabulary."
    level = record["cefrLevel"]
    band = record["generalFrenchFrequencyBand"]
    future = record["futureFrequency"]
    if record["word"] in COMMON_DISCOURSE:
        return "keep", "Common discourse word; do not treat a tagging error as difficulty."
    if level is None and band is None:
        return "ignore_or_gloss", "No reliable lexical match; review the tag before making it a teaching target."
    if level in {"A1", "A2"} or band == "common":
        return "keep", "Common learner vocabulary; leave the original word in place."
    if future >= 5:
        return "teach", "Recurs later in this volume, so learning it should pay off."
    if (level in {"C1", "C2"} or band == "rare") and future < 2:
        return "simplify", "Difficult and seldom seen later in this volume."
    if level in {"B1", "B2"} and future >= 2:
        return "teach", "Useful learner vocabulary that returns later."
    return "ignore_or_gloss", "Low recurrence; offer context without making it a learning target."


def build_records(chapters, counts, forms, flelex, lexique, chapter_number=1):
    records = []
    for (lemma, pos), chapter_count in counts[chapter_number].items():
        book_count = sum(counter[(lemma, pos)] for counter in counts.values())
        future = sum(counter[(lemma, pos)] for number, counter in counts.items() if number > chapter_number)
        lexeme_key = (lemma, "VERB" if pos == "AUX" else pos)
        frequency = lexique.get(lexeme_key)
        record = {
            "word": forms[(lemma, pos)].most_common(1)[0][0],
            "lemma": lemma,
            "partOfSpeech": pos,
            "chapterCount": chapter_count,
            "bookCount": book_count,
            "futureFrequency": future,
            "generalFrenchFrequency": frequency,
            "generalFrenchFrequencyBand": frequency_band(frequency),
            "cefrLevel": flelex.get(lexeme_key),
            "archaicOrLiterary": False,
            "properNoun": pos == "PROPN" or lemma in NAMES or any(form in NAMES for form in forms[(lemma, pos)]),
            "analysisConfidence": "lexical-match" if frequency is not None or flelex.get(lexeme_key) else "unmatched",
            "forms": [form for form, _ in forms[(lemma, pos)].most_common()],
        }
        record["archaicOrLiterary"] = (
            record["generalFrenchFrequencyBand"] == "rare" and future >= 2
        )
        record["classification"], record["reason"] = classify(record)
        records.append(record)
    return sorted(records, key=lambda row: (-row["chapterCount"], row["lemma"], row["partOfSpeech"]))


def find_glossary_record(headword, records):
    target = loose_fold(headword)
    options = [
        record for record in records
        if target == loose_fold(record["lemma"])
        or target in (loose_fold(form) for form in record["forms"])
    ]
    return max(options, key=lambda row: row["chapterCount"], default=None)


def enrich_glossary(glossary, records, chapter_text, later_text):
    for entry in glossary.values():
        headword = entry["headword"]
        record = find_glossary_record(headword, records)
        if record:
            for key in (
                "lemma", "partOfSpeech", "chapterCount", "bookCount", "futureFrequency",
                "generalFrenchFrequencyBand", "cefrLevel", "archaicOrLiterary",
                "properNoun", "classification", "reason", "forms",
            ):
                entry[key] = record[key]
        else:
            pattern = re.compile(r"(?<!\w)" + re.escape(loose_fold(headword)) + r"(?!\w)")
            chapter_count = len(pattern.findall(loose_fold(chapter_text)))
            future = len(pattern.findall(loose_fold(later_text)))
            entry.update({
                "lemma": fold(headword), "partOfSpeech": "X",
                "chapterCount": chapter_count, "bookCount": chapter_count + future,
                "futureFrequency": future, "generalFrenchFrequencyBand": None,
                "cefrLevel": None, "archaicOrLiterary": False,
                "properNoun": fold(headword) in NAMES, "forms": [headword],
                "classification": "ignore_or_gloss", "reason": "Curated contextual help.",
            })
        override = GLOSSARY_TREATMENT.get(fold(headword))
        if override:
            entry["classification"] = override
            entry["reason"] = {
                "simplify": "Specialized one-off nautical vocabulary; Plain mode can use familiar French.",
                "ignore_or_gloss": "Useful context here, but not an active vocabulary target.",
            }[override]
    return glossary


def difficulty_map(records):
    return {
        "target": "B1-ish, provisional",
        "rules": [
            "Names are lightly glossed, not treated as unknown vocabulary.",
            "Common A1/A2 words are kept.",
            "Words recurring at least five times later are teaching candidates.",
            "Rare high-level words with little recurrence are simplification candidates.",
            "Missing lexical data yields a light gloss, not a guessed CEFR level.",
        ],
        "counts": dict(Counter(record["classification"] for record in records)),
        "teach": sorted({record["lemma"] for record in records if record["classification"] == "teach"}),
        "simplify": sorted({record["lemma"] for record in records if record["classification"] == "simplify"}),
        "ignoreOrGloss": sorted({record["lemma"] for record in records if record["classification"] == "ignore_or_gloss"}),
    }
