# AI Story Transformer

A robust AI pipeline that reimagines classic stories in new universes.

## Overview
This system uses a 3-stage transformation pipeline:
1. **Extraction**: Distills the source story into an abstract "Transformation Contract".
2. **Mapping**: Reimagines the contract into the target context (e.g., Indian Education System).
3. **Generation**: Writes the final narrative based on the mapped outline.

## Key Files
- `story_transformer.py`: Core logic for the pipeline.
- `prompts.py`: Carefully engineered prompts for each stage.
- `run.py`: CLI entry point.
- `output/reimagined_story.md`: Sample output (Cinderella -> Kota Coaching Center).

## How to Run
Prerequisites: Python 3.8+, `groq` library.

1. **Set your API Key**:
   You need a Groq API key (from console.groq.com).
   ```powershell
   $env:GROQ_API_KEY = "gsk_..."
   ```

2. **Run the script**:
   ```powershell
   python run.py --source "Cinderella" --target "Indian Education System"
   ```
   
   To use your own story file:
   ```powershell
   python run.py --source ./my_story.txt --target "Cyberpunk 2077"
   ```

## Design Decisions
- **Transformation Contract**: We use a Pydantic model to enforce a strict schema for the story's essence, ensuring the AI doesn't just "rewrite" the text but "rebuilds" it.
- **Separation of Concerns**: Splitting Extraction, Mapping, and Generation allows for better debugging and steerability.
