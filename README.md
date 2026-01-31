# Wikipedia Translator

A desktop app that translates Wikipedia articles **between any language pair** using AI (Gemini). It keeps wikitext structure intact so you can copy or save the result and edit directly on your language’s Wikipedia.

---

## Why this exists

**Wikipedia is one of the world’s biggest knowledge bases**, but its content is very uneven across languages.

- **English has far more articles.** When you search in your own language, you often find nothing—even though the same topic exists in English. That gap locks a lot of people out of knowledge.
- **The reverse happens too.** Some articles exist only in your language (local history, culture, figures) and have no English version. Sharing that knowledge with the world is harder.
- **Adults with time, tools, and language skills** can use machine translation, AI, or learn another language. But many others are left behind:
  - People who don’t have a “talent” for languages  
  - Kids who want to understand a topic in their mother tongue  
  - Anyone who simply prefers or needs content in their own language  

This project is a small step to **bridge that gap**: translate Wikipedia articles between any two languages with AI, preserve wikitext so the result can be used on Wikipedia, and make it easier for more people to access and contribute knowledge in their language.

---

## Features

- **Fetch wikitext** — Paste a Wikipedia article URL (any language). The app fetches the source wikitext via the MediaWiki REST API.
- **Translate with Gemini** — Choose source and target languages (e.g. English → Vietnamese, German → Japanese). Translation keeps wikitext syntax (templates, links, refs, tables, headings).
- **Long articles** — Articles are split by sections or size, translated in chunks, then merged. Large context windows are used so fewer API calls are needed.
- **AI check** — Run an AI-powered check (layout, content alignment, terminology, internal links). Uses the same Gemini API; works for any language pair.
- **Export** — Copy target wikitext to the clipboard or save to a file (`.wiki` or `.txt`).
- **GUI** — Simple desktop UI (tkinter), File/Help menu, tooltips, background tasks so the interface stays responsive. Interface available in English and Vietnamese.

---

## Requirements

- **Python** 3.10 or newer  
- **OS** — Windows, macOS, or Linux (tkinter is usually included with Python; on Linux you may need `python3-tk`)  
- **Gemini API key** — Free at [Google AI Studio](https://aistudio.google.com/apikey)

---

## Installation

1. Clone or download this repository.

2. (Recommended) Create a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate   # macOS / Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

- **Gemini API key** — Enter it in the app’s “API key” field. It can be saved in `config/config.json` (saved automatically when you translate). Do not commit this file (it’s in `.gitignore`).
- **Model** — Choose in the dropdown (e.g. `gemini-3-flash-preview`, `gemini-3-pro-preview`; depends on API availability).
- **Language pair** — Select “From” and “To” languages in the UI (e.g. English → Vietnamese). The same pair is used for translation and for the AI check.

---

## Run the app

From the project root:

```bash
python -m src.main
```

Or:

```bash
python src/main.py
```

If you get import errors, run from the project root and use `python -m src.main`.

---

## How to use

1. Choose **From** and **To** languages (e.g. English → Vietnamese).
2. Paste a **Wikipedia article URL** (any language, e.g. `https://en.wikipedia.org/wiki/...`).
3. Click **Fetch wikitext** — source wikitext appears in the top box.
4. Enter your **Gemini API key** (if not already saved), choose a **model**, then click **Translate** — target wikitext appears in the bottom box.
5. (Optional) Click **Check** — AI analyzes layout, content, terminology, and links; report is shown below.
6. Edit the target wikitext by hand if needed, then **Copy** or **Save to file** (or **File → Save target wikitext...**). Use the result on your language’s Wikipedia or keep it for your own use.

---

## Project structure

```
automatic-wikipedia-translation/
├── config/                 # config.json (API key, model, lang) — do not commit
│   └── .gitkeep
├── src/
│   ├── main.py             # Entry point, launches GUI
│   ├── config_loader.py   # Load/save config
│   ├── languages.py       # Language list for UI
│   ├── gui/
│   │   ├── app.py         # Main window
│   │   ├── frames.py     # Frames (link, config, log, wikitext, export, check result)
│   │   ├── dialogs.py    # Dialogs, tooltips
│   │   ├── i18n.py       # Strings (EN / VI)
│   │   └── background.py # Background tasks (threading)
│   ├── wikipedia/
│   │   └── fetch.py      # Parse URL, MediaWiki REST API → wikitext
│   ├── translate/
│   │   ├── gemini_client.py  # Translate wikitext (any pair), chunking
│   │   └── chunker.py        # Split by section / size
│   └── check/
│       ├── ai_check.py   # AI check (layout, content, terminology, links)
│       ├── layout.py    # (Legacy) layout rules
│       ├── content.py   # (Legacy) content comparison
│       └── normalize.py  # (Legacy) glossary normalize
├── .gitignore
├── requirements.txt
└── README.md
```

---

## License

This project is for reference and sharing. See the repository for terms of use.
