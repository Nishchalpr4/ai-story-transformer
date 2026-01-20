# 🎭 AI Story Transformer

Transform classic stories into new cultural contexts using AI prompt chaining.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What It Does

Takes any story and reimagines it in a completely different setting while preserving the narrative structure. 

**Example:** Cinderella → Indian Education System
- The Ball → Scholarship Exam
- Fairy Godmother → Wise Teacher/Mentor  
- Glass Slipper → Academic Excellence
- Prince → Supportive Fellow Student

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/story-transformer.git
cd story-transformer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your API key

Get a free API key from [console.groq.com](https://console.groq.com)

**Option A: Create a `.env` file**
```bash
cp .env.example .env
# Edit .env and add your key
```

**Option B: Set environment variable**
```bash
# Windows PowerShell
$env:GROQ_API_KEY = "your-api-key-here"

# Linux/Mac
export GROQ_API_KEY="your-api-key-here"
```

### 4. Run the transformer

```bash
python run.py
```

You'll be prompted to select an output style (Narrative, Screenplay, Satirical, or Epic).

---

## How It Works

The transformer uses a 3-stage prompt chain:

```
Stage 1: EXTRACT          Stage 2: MAP              Stage 3: GENERATE
   │                         │                         │
   ▼                         ▼                         ▼
Story Essence      →     Story Map         →      Final Story
(themes, archetypes,     (new characters,         (1000+ words in
 plot beats)              settings, plot)          chosen style)
```

Each stage builds on the output of the previous one, ensuring coherent transformation.

---

## Project Structure

```
story-transformer/
├── run.py                 # Entry point - run this
├── story_transformer.py   # Core transformation pipeline
├── prompts.py             # Prompt templates for each stage
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
└── output/                # Generated stories saved here
```

---

## Features

- **3-Stage Pipeline** — Extract → Map → Generate for coherent results
- **Structured Output** — Pydantic models ensure valid LLM responses
- **Multiple Styles** — Narrative, Screenplay, Satirical, or Epic
- **Automatic Retries** — Handles API failures gracefully
- **Input Validation** — Validates all inputs before processing

---

## Tech Stack

- **LLM**: Llama 3.3 70B via Groq (fast inference)
- **Validation**: Pydantic v2
- **Python**: 3.8+

---

## License

MIT License — see [LICENSE](LICENSE) for details.
