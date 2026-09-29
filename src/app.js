const STORAGE_KEY = "multi-read-v0.1";
const CHAPTER_URL = "data/monte-cristo/c01.json";
const CHAPTER_WRAPPER_URL = "data/monte-cristo/c01.js";
const difficultyOrder = ["plain", "guided", "original"];

let activeChapter = null;
let glossary = {};
let passages = [];

const els = {
  title: document.querySelector("#title"),
  subtitle: document.querySelector("#subtitle"),
  sourceMeta: document.querySelector("#sourceMeta"),
  modeButtons: document.querySelector("#modeButtons"),
  passageText: document.querySelector("#passageText"),
  comparison: document.querySelector("#comparison"),
  comparisonText: document.querySelector("#comparisonText"),
  helpPanel: document.querySelector("#helpPanel"),
  helpTitle: document.querySelector("#helpTitle"),
  helpBody: document.querySelector("#helpBody"),
  helpNote: document.querySelector("#helpNote"),
  learnerStats: document.querySelector("#learnerStats"),
  recommendation: document.querySelector("#recommendation"),
  eventLog: document.querySelector("#eventLog"),
  compareToggle: document.querySelector("#compareToggle"),
  resetButton: document.querySelector("#resetButton"),
  previousPassage: document.querySelector("#previousPassage"),
  nextPassage: document.querySelector("#nextPassage"),
  passageProgress: document.querySelector("#passageProgress"),
  chapterStatus: document.querySelector("#chapterStatus")
};

const state = loadState();

loadChapter().then((chapter) => {
  activeChapter = chapter;
  glossary = chapter.glossary;
  passages = chapter.passages;
  render();
}).catch((error) => {
  console.error(error);
  els.subtitle.textContent = "Chapter data could not be loaded.";
  els.passageText.innerHTML = `<p class="load-error">Could not load ${escapeHtml(CHAPTER_URL)}. Use the vault dashboard URL or regenerate the chapter data.</p>`;
});

function loadState() {
  const fallback = {
    mode: "guided",
    passageIndex: 0,
    events: [],
    translationsOpen: [],
    currentHelp: null,
    compareOpen: false
  };

  try {
    return { ...fallback, ...JSON.parse(localStorage.getItem(STORAGE_KEY)) };
  } catch {
    return fallback;
  }
}

async function loadChapter() {
  if (location.protocol === "http:" || location.protocol === "https:") {
    const response = await fetch(CHAPTER_URL);
    if (!response.ok) {
      throw new Error(`Failed to load ${CHAPTER_URL}: ${response.status}`);
    }
    return response.json();
  }

  if (window.MultiReadChapter) {
    return window.MultiReadChapter;
  }

  await loadScript(CHAPTER_WRAPPER_URL);
  if (window.MultiReadChapter) {
    return window.MultiReadChapter;
  }

  throw new Error("No chapter data available for this protocol.");
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = src;
    script.onload = resolve;
    script.onerror = () => reject(new Error(`Failed to load ${src}`));
    document.head.appendChild(script);
  });
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function getPassage() {
  if (!passages[state.passageIndex]) {
    state.passageIndex = 0;
  }
  return passages[state.passageIndex];
}

function recordEvent(type, payload = {}) {
  state.events.unshift({
    type,
    payload,
    mode: state.mode,
    at: new Date().toISOString()
  });
  state.events = state.events.slice(0, 25);
  saveState();
  renderModel();
}

function tokenize(text) {
  const targetWords = Object.keys(glossary).sort((a, b) => b.length - a.length);
  let html = escapeHtml(text);

  for (const key of targetWords) {
    const label = glossary[key].headword;
    const escapedLabel = escapeHtml(label);
    const pattern = new RegExp(`\\b${escapeRegExp(label)}\\b`, "gi");
    html = html.replace(pattern, (match) => {
      return `<button class="word-help" data-key="${key}" type="button">${match}</button>`;
    });

    if (key.includes("-") && key.replaceAll("-", " ") !== label.toLowerCase()) {
      const spaced = key.replaceAll("-", " ");
      const spacedPattern = new RegExp(escapeRegExp(spaced), "gi");
      html = html.replace(spacedPattern, (match) => {
        return `<button class="word-help" data-key="${key}" type="button">${match}</button>`;
      });
    }

    if (!html.includes(`data-key="${key}"`) && text.toLowerCase().includes(label.toLowerCase())) {
      html = html.replace(escapedLabel, `<button class="word-help" data-key="${key}" type="button">${escapedLabel}</button>`);
    }
  }

  return html;
}

function render() {
  const passage = getPassage();
  const current = passage.representations[state.mode];
  els.title.textContent = passage.book;
  els.subtitle.textContent = `${passage.title} · ${current.label} · ${current.level}`;
  els.sourceMeta.textContent = `${passage.sourceEpub} · ${passage.sourceChapter}`;
  els.previousPassage.disabled = state.passageIndex === 0;
  els.nextPassage.disabled = state.passageIndex === passages.length - 1;
  els.passageProgress.textContent = `Passage ${state.passageIndex + 1} of ${passages.length}`;
  els.chapterStatus.textContent = state.passageIndex === passages.length - 1
    ? `End of processed Chapter ${activeChapter.chapterNumber}. Need to process ${activeChapter.nextChapterId?.toUpperCase() ?? "the next chapter"}.`
    : `Chapter ${activeChapter.chapterNumber} processed first pass. Notes go in project/ideas/feeback-c01.md.`;

  els.modeButtons.innerHTML = difficultyOrder.map((mode) => {
    const item = passage.representations[mode];
    const selected = mode === state.mode ? "true" : "false";
    return `<button class="mode-button" type="button" aria-pressed="${selected}" data-mode="${mode}">
      <span>${item.label}</span>
      <small>${item.level}</small>
    </button>`;
  }).join("");

  els.passageText.innerHTML = current.sentences.map((sentence) => {
    const isOpen = state.translationsOpen.includes(sentence.id);
    const hasTranslation = Boolean(sentence.translation);
    return `<article class="sentence" data-sentence="${sentence.id}">
      <p>${tokenize(sentence.text)}</p>
      <div class="sentence-actions">
        <button class="text-button translation-toggle" type="button" data-sentence="${sentence.id}">
          ${isOpen ? "Hide meaning" : hasTranslation ? "Show meaning" : "Check meaning"}
        </button>
      </div>
      <p class="translation ${isOpen ? "is-open" : ""}">${escapeHtml(sentence.translation || "Sentence meaning has not been processed for this chapter yet. Add this to feeback-c01.md if sentence-level meaning should be generated for C02.")}</p>
    </article>`;
  }).join("");

  els.compareToggle.checked = state.compareOpen;
  els.comparison.hidden = !state.compareOpen;
  els.comparisonText.innerHTML = passage.originalComparison.map((line) => `<p>${escapeHtml(line)}</p>`).join("");

  bindInteractions();
  renderHelp();
  renderModel();
}

function bindInteractions() {
  els.modeButtons.querySelectorAll("button").forEach((button) => {
    button.addEventListener("click", () => {
      const nextMode = button.dataset.mode;
      if (nextMode === state.mode) return;
      state.mode = nextMode;
      state.translationsOpen = [];
      recordEvent("mode_change", { mode: nextMode });
      saveState();
      render();
    });
  });

  els.passageText.querySelectorAll(".word-help").forEach((button) => {
    button.addEventListener("click", () => {
      state.currentHelp = button.dataset.key;
      recordEvent("lookup", { key: button.dataset.key });
      renderHelp();
    });
  });

  els.passageText.querySelectorAll(".translation-toggle").forEach((button) => {
    button.addEventListener("click", () => {
      const sentenceId = button.dataset.sentence;
      if (state.translationsOpen.includes(sentenceId)) {
        state.translationsOpen = state.translationsOpen.filter((id) => id !== sentenceId);
      } else {
        state.translationsOpen.push(sentenceId);
        recordEvent("translation", { sentenceId });
      }
      saveState();
      render();
    });
  });
}

function renderHelp() {
  const entry = glossary[state.currentHelp];

  if (!entry) {
    els.helpTitle.textContent = "Tap a highlighted word";
    els.helpBody.textContent = "Contextual help appears here without taking you away from the passage.";
    els.helpNote.textContent = "Lookups are counted locally as a friction signal.";
    return;
  }

  els.helpTitle.textContent = entry.headword;
  els.helpBody.textContent = entry.meaning;
  els.helpNote.textContent = entry.note;
}

function renderModel() {
  const passage = getPassage();
  const counts = getCounts();
  const recommendation = recommend(counts);

  els.learnerStats.innerHTML = `
    <li><strong>${counts.lookups}</strong><span>lookups</span></li>
    <li><strong>${counts.translations}</strong><span>translations</span></li>
    <li><strong>${counts.modeChanges}</strong><span>level changes</span></li>
    <li><strong>${passage.representations[state.mode].label}</strong><span>current text</span></li>
  `;

  els.recommendation.innerHTML = `
    <strong>${recommendation.title}</strong>
    <span>${recommendation.body}</span>
  `;

  els.eventLog.innerHTML = state.events.length
    ? state.events.slice(0, 8).map((event) => `<li>${formatEvent(event)}</li>`).join("")
    : "<li>No reading events yet.</li>";
}

function getCounts() {
  return state.events.reduce((counts, event) => {
    if (event.type === "lookup") counts.lookups += 1;
    if (event.type === "translation") counts.translations += 1;
    if (event.type === "mode_change") counts.modeChanges += 1;
    return counts;
  }, { lookups: 0, translations: 0, modeChanges: 0 });
}

function recommend(counts) {
  const passage = getPassage();
  const currentIndex = difficultyOrder.indexOf(state.mode);
  const friction = counts.lookups + counts.translations * 2;

  if (friction >= 5 && currentIndex > 0) {
    const easier = passage.representations[difficultyOrder[currentIndex - 1]].label;
    return {
      title: `Try ${easier} next`,
      body: "Several help requests suggest the current representation is costing attention."
    };
  }

  if (friction <= 1 && currentIndex < difficultyOrder.length - 1) {
    const harder = passage.representations[difficultyOrder[currentIndex + 1]].label;
    return {
      title: `Try ${harder} next`,
      body: "Very little help was needed, so the next harder representation may be productive."
    };
  }

  return {
    title: "Stay here",
    body: "The signal is mixed or still sparse. Keep reading at this representation."
  };
}

function formatEvent(event) {
  const passage = getPassage();
  const time = new Date(event.at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  if (event.type === "lookup") return `${time}: looked up ${glossary[event.payload.key]?.headword ?? event.payload.key}`;
  if (event.type === "translation") return `${time}: opened sentence meaning`;
  if (event.type === "mode_change") return `${time}: changed to ${passage.representations[event.payload.mode].label}`;
  if (event.type === "passage_change") return `${time}: moved to passage ${event.payload.passageIndex + 1}`;
  return `${time}: ${event.type}`;
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#039;"
  })[char]);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

els.compareToggle.addEventListener("change", () => {
  state.compareOpen = els.compareToggle.checked;
  recordEvent("compare_toggle", { visible: state.compareOpen });
  saveState();
  render();
});

els.previousPassage.addEventListener("click", () => {
  if (state.passageIndex === 0) return;
  state.passageIndex -= 1;
  state.translationsOpen = [];
  state.currentHelp = null;
  recordEvent("passage_change", { passageIndex: state.passageIndex });
  saveState();
  render();
});

els.nextPassage.addEventListener("click", () => {
  if (state.passageIndex >= passages.length - 1) return;
  state.passageIndex += 1;
  state.translationsOpen = [];
  state.currentHelp = null;
  recordEvent("passage_change", { passageIndex: state.passageIndex });
  saveState();
  render();
});

els.resetButton.addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  window.location.reload();
});
