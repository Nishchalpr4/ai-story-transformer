# 🎭 AI Story Transformer

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Transform classic stories into new cultural contexts using AI prompt chaining.

**Demo:** Takes Cinderella and reimagines it in the Indian Education System — turning the ball into a scholarship exam, the Fairy Godmother into a wise professor, and the Prince into a top-ranking student.

---

## 🧠 How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        3-STAGE PROMPT CHAIN                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │   STAGE 1    │     │   STAGE 2    │     │   STAGE 3    │            │
│  │   EXTRACT    │────▶│     MAP      │────▶│   GENERATE   │            │
│  └──────────────┘     └──────────────┘     └──────────────┘            │
│         │                   │                    │                      │
│         ▼                   ▼                    ▼                      │
│   StoryEssence         StoryMap            Final Story                 │
│   (archetypes,         (new names,         (1000+ words,               │
│    themes,              settings,           chosen style)              │
│    plot beats)          plot outline)                                   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Prompt Chaining** | 3-stage pipeline where each stage builds on the previous |
| **Structured Output** | Pydantic models ensure valid, typed LLM responses |
| **Multiple Styles** | Narrative, Screenplay, Satirical, or Epic |
| **Retry Logic** | Automatic retries on API failures |
| **Input Validation** | Validates story, target, and style inputs |

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/story-transformer.git
cd story-transformer
pip install -r requirements.txt
```

### 2. Set API Key

Get a free API key from [console.groq.com](https://console.groq.com)

```bash
# Windows PowerShell
$env:GROQ_API_KEY = "your-key-here"

# Linux/Mac
export GROQ_API_KEY="your-key-here"
```

### 3. Run

```bash
python run.py
```

---

## 📁 Project Structure

```
story-transformer/
├── run.py                 # Entry point with CLI
├── story_transformer.py   # Core 3-stage pipeline
├── prompts.py             # Prompt templates for each stage
├── requirements.txt       # Dependencies
├── .env.example           # Environment template
└── output/
    └── story.md           # Generated story output
```

---

## 🔧 Technical Details

### Why 3 Stages?

| Approach | Problem |
|----------|---------|
| Single prompt | Shallow find-and-replace, loses story structure |
| **3-stage chain** | Extracts DNA → Maps to new world → Writes coherently |

### Why Pydantic?

```python
class Character(BaseModel):
    name: str
    archetype: str    # Enforced structure
    role: str         # LLM can't return garbage
    motivation: str
```

LLMs can hallucinate malformed JSON. Pydantic catches this immediately.

---

## 📊 Example Transformation

| Original (Cinderella) | → | Transformed (Indian Education) |
|----------------------|---|--------------------------------|
| Cinderella | → | Riya (brilliant but poor student) |
| Stepmother | → | Strict joint family elders |
| Fairy Godmother | → | Professor Sharma (mentor) |
| Glass Slipper | → | Perfect exam score |
| The Ball | → | IIT-JEE examination |
| Prince | → | Recognition & scholarship |

---

## 🛠️ Tech Stack

- **LLM**: Llama 3.3 70B via Groq (fast inference)
- **Validation**: Pydantic v2
- **Python**: 3.8+

---

## 📝 License

MIT License - feel free to use and modify.

---

## 🤝 Why I Built This

This project demonstrates:
- **Prompt Engineering** — Carefully designed prompts for each stage
- **Prompt Chaining** — Output of one stage feeds into the next
- **Structured LLM Output** — Using Pydantic for reliable data extraction
- **Production Patterns** — Error handling, retries, logging, validation

Built as a demonstration of AI engineering best practices.
