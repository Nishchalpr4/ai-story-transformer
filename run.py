"""
Story Transformer - Main Entry Point
=====================================
Transforms classic stories into new cultural contexts using AI.

Example: Cinderella → Indian Education System

Usage:
    python run.py
"""

import os
import sys
import time
import logging
from story_transformer import StoryTransformer, TransformationError
from dotenv import load_dotenv

load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# SAMPLE STORY
# ============================================================================

CINDERELLA = """
Once upon a time, there was a young girl named Cinderella. She lived with her 
wicked stepmother and two ugly stepsisters who treated her like a servant. 
One day, the King announced a grand ball to find a bride for the Prince. 
Cinderella wanted to go, but her stepfamily forbade it and ruined her dress.

A Fairy Godmother appeared and transformed a pumpkin into a carriage, mice 
into horses, and her rags into a beautiful gown with glass slippers. She 
warned Cinderella the magic would end at midnight.

At the ball, the Prince fell in love with her. They danced all night. As the 
clock struck twelve, she fled, losing one glass slipper.

The Prince searched the kingdom. The stepsisters tried to force the shoe on, 
but it only fit Cinderella. The Prince recognized her, they married, and 
lived happily ever after.
"""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_api_key():
    """Retrieve API key from environment variables."""
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        print("Error: GROQ_API_KEY not found in environment.")
        print("Set it with: $env:GROQ_API_KEY = 'your-key-here'")
        sys.exit(1)
    return key


def select_style():
    """Display style menu and get user selection."""
    styles = {"1": "narrative", "2": "screenplay", "3": "satirical", "4": "epic"}
    
    print("\nSelect output style:")
    print("  [1] Narrative   - Traditional prose story")
    print("  [2] Screenplay  - Movie script format")
    print("  [3] Satirical   - Humorous/ironic take")
    print("  [4] Epic        - Grand, dramatic style")
    
    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"
    selected = styles.get(choice, "narrative")
    print(f"Selected: {selected}\n")
    return selected


def save_story(results, output_dir="output"):
    """Save the generated story to a markdown file."""
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, "story.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {results['map'].new_title}\n\n")
        f.write(results["story"])
    
    print(f"\nStory saved to: {filepath}")
    return filepath


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run the story transformation pipeline."""
    print("=" * 50)
    print("AI STORY TRANSFORMER")
    print("=" * 50)
    
    start_time = time.time()
    
    try:
        # Setup
        api_key = get_api_key()
        style = select_style()
        
        # Transform
        logger.info("Starting transformation pipeline...")
        transformer = StoryTransformer(api_key)
        results = transformer.transform(
            story=CINDERELLA,
            target="Indian Education System",
            style=style
        )
        
        # Save
        save_story(results)
        
        # Stats
        elapsed = time.time() - start_time
        logger.info(f"Completed in {elapsed:.1f} seconds")
        print("\nDone!")
        
    except TransformationError as e:
        logger.error(f"Transformation failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
