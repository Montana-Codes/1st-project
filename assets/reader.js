(function () {
  let pdfJsModulePromise;

  const NT_BOOKS = [
    ["Matthew", 28],
    ["Mark", 16],
    ["Luke", 24],
    ["John", 21],
    ["Acts", 28],
    ["Romans", 16],
    ["1 Corinthians", 16],
    ["2 Corinthians", 13],
    ["Galatians", 6],
    ["Ephesians", 6],
    ["Philippians", 4],
    ["Colossians", 4],
    ["1 Thessalonians", 5],
    ["2 Thessalonians", 3],
    ["1 Timothy", 6],
    ["2 Timothy", 4],
    ["Titus", 3],
    ["Philemon", 1],
    ["Hebrews", 13],
    ["James", 5],
    ["1 Peter", 5],
    ["2 Peter", 3],
    ["1 John", 5],
    ["2 John", 1],
    ["3 John", 1],
    ["Jude", 1],
    ["Revelation", 22],
  ];

  const state = {
    selectedBook: NT_BOOKS[0][0],
    selectedChapter: 1,
    syncScroll: true,
    niv: { text: "", loaded: false, fileName: "" },
    cuv: { text: "", loaded: false, fileName: "" },
  };

  const elements = {
    bookSelect: document.getElementById("bookSelect"),
    chapterSelect: document.getElementById("chapterSelect"),
    prevButton: document.getElementById("prevChapter"),
    nextButton: document.getElementById("nextChapter"),
    syncScroll: document.getElementById("syncScroll"),
    message: document.getElementById("readerMessage"),
    nivPane: document.getElementById("nivPane"),
    cuvPane: document.getElementById("cuvPane"),
    nivFile: document.getElementById("nivFile"),
    cuvFile: document.getElementById("cuvFile"),
    nivStatus: document.getElementById("nivStatus"),
    cuvStatus: document.getElementById("cuvStatus"),
  };

  function setMessage(message, isError) {
    elements.message.textContent = message;
    elements.message.classList.toggle("error", Boolean(isError));
  }

  function populateBookSelector() {
    elements.bookSelect.innerHTML = NT_BOOKS.map(
      ([name]) => `<option value="${name}">${name}</option>`
    ).join("");
    elements.bookSelect.value = state.selectedBook;
  }

  function updateChapterSelector() {
    const maxChapter = NT_BOOKS.find(([book]) => book === state.selectedBook)?.[1] || 1;
    if (state.selectedChapter > maxChapter) {
      state.selectedChapter = maxChapter;
    }

    elements.chapterSelect.innerHTML = Array.from(
      { length: maxChapter },
      (_, index) => `<option value="${index + 1}">${index + 1}</option>`
    ).join("");
    elements.chapterSelect.value = String(state.selectedChapter);

    elements.prevButton.disabled = state.selectedBook === NT_BOOKS[0][0] && state.selectedChapter === 1;
    const [lastBook, lastChapter] = NT_BOOKS[NT_BOOKS.length - 1];
    elements.nextButton.disabled =
      state.selectedBook === lastBook && state.selectedChapter === lastChapter;
  }

  function findTextAnchor(text, book, chapter) {
    if (!text) {
      return -1;
    }

    const escapedBook = book.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const candidates = [
      new RegExp(`${escapedBook}\\s+${chapter}\\b`, "i"),
      new RegExp(`${escapedBook}${chapter}\\b`, "i"),
      new RegExp(`\\bChapter\\s+${chapter}\\b`, "i"),
      new RegExp(`\\bCHAPTER\\s+${chapter}\\b`, "i"),
    ];

    for (const candidate of candidates) {
      const match = text.match(candidate);
      if (match?.index !== undefined) {
        return match.index;
      }
    }

    return -1;
  }

  function createDisplayText(text, startIndex) {
    if (!text) {
      return "";
    }

    const chunks = text
      .slice(Math.max(0, startIndex || 0))
      .replace(/\r/g, "")
      .split(/\n{2,}/)
      .map((chunk) => chunk.trim())
      .filter(Boolean);

    return chunks.slice(0, 800).join("\n\n");
  }

  function renderPane(pane, translationKey) {
    const translation = state[translationKey];
    pane.innerHTML = "";

    if (!translation.loaded || !translation.text) {
      pane.innerHTML =
        translationKey === "niv"
          ? `<div class="empty-state"><p><strong>NIV is empty.</strong></p><p>Import a legally obtained NIV New Testament PDF/EPUB to begin.</p></div>`
          : `<div class="empty-state"><p><strong>CUV is empty.</strong></p><p>Import a legally obtained Chinese Union Version New Testament PDF/EPUB to begin.</p></div>`;
      return null;
    }

    const heading = document.createElement("p");
    heading.className = "chapter-marker";
    heading.textContent = `${state.selectedBook} ${state.selectedChapter}`;

    const anchor = findTextAnchor(translation.text, state.selectedBook, state.selectedChapter);
    const content = document.createElement("div");
    content.textContent = createDisplayText(translation.text, anchor >= 0 ? anchor : 0);

    pane.appendChild(heading);
    pane.appendChild(content);
    return anchor >= 0;
  }

  function renderAllPanes() {
    const nivAnchorFound = renderPane(elements.nivPane, "niv");
    const cuvAnchorFound = renderPane(elements.cuvPane, "cuv");
    const hasLoadedFiles = state.niv.loaded || state.cuv.loaded;
    const anchorMissing =
      (state.niv.loaded && nivAnchorFound === false) || (state.cuv.loaded && cuvAnchorFound === false);

    if (!hasLoadedFiles) {
      setMessage(
        "Choose NIV and CUV New Testament PDF/EPUB files to start reading side-by-side.",
        false
      );
      return;
    }

    if (anchorMissing) {
      setMessage(
        "Files loaded. Chapter navigation is best-effort because PDF/EPUB formatting differs by publisher.",
        false
      );
      return;
    }

    setMessage("Import complete. Your files stay on this device and are not uploaded.", false);
  }

  async function extractPdfText(file) {
    if (!pdfJsModulePromise) {
      pdfJsModulePromise = import(
        "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.6.82/build/pdf.min.mjs"
      );
    }
    const pdfModule = await pdfJsModulePromise;
    const pdfjs = pdfModule.default || pdfModule;
    pdfjs.GlobalWorkerOptions.workerSrc =
      "https://cdn.jsdelivr.net/npm/pdfjs-dist@4.6.82/build/pdf.worker.min.mjs";

    const bytes = await file.arrayBuffer();
    const documentRef = await pdfjs.getDocument({ data: bytes }).promise;

    let text = "";
    for (let pageNumber = 1; pageNumber <= documentRef.numPages; pageNumber += 1) {
      const page = await documentRef.getPage(pageNumber);
      const content = await page.getTextContent();
      const pageText = content.items.map((item) => item.str).join(" ");
      text += `\n${pageText}`;
    }

    return text;
  }

  async function extractEpubText(file) {
    if (typeof window.ePub !== "function") {
      throw new Error("EPUB support library could not be loaded.");
    }

    const bytes = await file.arrayBuffer();
    const book = window.ePub(bytes);
    await book.ready;

    let text = "";
    for (const section of book.spine.spineItems) {
      const sectionDocument = await section.load(book.load.bind(book));
      text += `\n${sectionDocument?.body?.innerText || ""}`;
      section.unload();
    }

    return text;
  }

  async function extractText(file) {
    const extension = file.name.split(".").pop()?.toLowerCase();
    if (extension === "pdf") {
      return extractPdfText(file);
    }
    if (extension === "epub") {
      return extractEpubText(file);
    }

    throw new Error("Unsupported file type. Please choose a .pdf or .epub file.");
  }

  async function handleImport(translationKey, file) {
    const statusEl = translationKey === "niv" ? elements.nivStatus : elements.cuvStatus;

    if (!file) {
      return;
    }

    statusEl.textContent = `Loading ${file.name}...`;
    setMessage("", false);

    try {
      const text = await extractText(file);
      state[translationKey].text = text;
      state[translationKey].loaded = true;
      state[translationKey].fileName = file.name;
      statusEl.textContent = `Loaded ${file.name}. Displaying imported text locally in your browser.`;
      renderAllPanes();
    } catch (error) {
      state[translationKey].loaded = false;
      state[translationKey].text = "";
      statusEl.textContent = `Could not load ${file.name}.`;
      renderAllPanes();
      setMessage(error.message || "Could not parse this file.", true);
    }
  }

  function moveChapter(offset) {
    let bookIndex = NT_BOOKS.findIndex(([book]) => book === state.selectedBook);
    let chapter = state.selectedChapter + offset;

    while (bookIndex >= 0 && bookIndex < NT_BOOKS.length) {
      const [, maxChapter] = NT_BOOKS[bookIndex];

      if (chapter >= 1 && chapter <= maxChapter) {
        state.selectedBook = NT_BOOKS[bookIndex][0];
        state.selectedChapter = chapter;
        break;
      }

      if (chapter < 1) {
        bookIndex -= 1;
        if (bookIndex < 0) {
          return;
        }
        chapter = NT_BOOKS[bookIndex][1];
      } else {
        chapter = chapter - maxChapter;
        bookIndex += 1;
      }
    }

    elements.bookSelect.value = state.selectedBook;
    updateChapterSelector();
    renderAllPanes();
  }

  function setupScrollSync() {
    let syncing = false;

    function sync(source, target) {
      if (!state.syncScroll || syncing) {
        return;
      }

      const sourceRange = source.scrollHeight - source.clientHeight;
      const targetRange = target.scrollHeight - target.clientHeight;
      if (sourceRange <= 0 || targetRange <= 0) {
        return;
      }

      syncing = true;
      target.scrollTop = (source.scrollTop / sourceRange) * targetRange;
      requestAnimationFrame(() => {
        syncing = false;
      });
    }

    elements.nivPane.addEventListener("scroll", () => sync(elements.nivPane, elements.cuvPane));
    elements.cuvPane.addEventListener("scroll", () => sync(elements.cuvPane, elements.nivPane));
  }

  function setupEvents() {
    elements.bookSelect.addEventListener("change", (event) => {
      state.selectedBook = event.target.value;
      state.selectedChapter = 1;
      updateChapterSelector();
      renderAllPanes();
    });

    elements.chapterSelect.addEventListener("change", (event) => {
      state.selectedChapter = Number(event.target.value);
      updateChapterSelector();
      renderAllPanes();
    });

    elements.prevButton.addEventListener("click", () => moveChapter(-1));
    elements.nextButton.addEventListener("click", () => moveChapter(1));

    elements.syncScroll.addEventListener("change", (event) => {
      state.syncScroll = event.target.checked;
      setMessage(
        state.syncScroll
          ? "Scroll sync enabled."
          : "Scroll sync disabled. You can scroll each column independently.",
        false
      );
    });

    elements.nivFile.addEventListener("change", (event) => handleImport("niv", event.target.files?.[0]));
    elements.cuvFile.addEventListener("change", (event) => handleImport("cuv", event.target.files?.[0]));
  }

  function init() {
    populateBookSelector();
    updateChapterSelector();
    setupEvents();
    setupScrollSync();
    renderAllPanes();
  }

  init();
})();
