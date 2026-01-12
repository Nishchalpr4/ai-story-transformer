"""
AI Story Transformer - Command Line Interface
==============================================
This script is the ENTRY POINT of the application.
Run it from terminal: python run.py --source "Cinderella" --target "Space Opera"
"""

import argparse
import os
import sys
import json
from datetime import datetime
from story_transformer import StoryTransformer
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()


# ============================================================================
# DEFAULT STORY - Used when no story file is provided
# ============================================================================
DEFAULT_CINDERELLA_STORY = """
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
# STEP 1: GET API KEY
# ============================================================================
def get_api_key(args):
    """
    Get the Groq API key from command line OR environment variable.
    
    Priority: command line > GROQ_API_KEY env var > groq_api_key env var
    """
    api_key = args.api_key or os.environ.get("GROQ_API_KEY") or os.environ.get("groq_api_key")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found!")
        print("   Set it with: $env:GROQ_API_KEY = 'your_key_here'")
        sys.exit(1)
    
    return api_key


# ============================================================================
# STEP 2: LOAD THE SOURCE STORY
# ============================================================================
def load_source_story(source_arg):
    """
    Load the story from one of 3 possible sources:
    1. A file path (e.g., "./my_story.txt")
    2. The keyword "Cinderella" (uses built-in story)
    3. Raw story text passed directly
    """
    # Option 1: It's a file path
    if os.path.exists(source_arg):
        print(f"📖 Loading story from file: {source_arg}")
        with open(source_arg, "r") as f:
            return f.read()
    
    # Option 2: It's the keyword "Cinderella"
    if source_arg.lower() == "cinderella":
        print("📖 Using built-in Cinderella story")
        return DEFAULT_CINDERELLA_STORY
    
    # Option 3: It's raw text (if long enough to be a story)
    if len(source_arg) > 50:
        print("📖 Using provided text as story")
        return source_arg
    
    # None of the above - error!
    print(f"❌ Error: '{source_arg}' is not a valid file or story text")
    sys.exit(1)


# ============================================================================
# STEP 3: LET USER CHOOSE STYLE INTERACTIVELY
# ============================================================================
def choose_style(style_arg):
    """
    Let user choose output style interactively if not provided via CLI.
    """
    STYLES = {
        "1": ("narrative", "Classic prose with rich descriptions"),
        "2": ("screenplay", "Film screenplay format with scenes & dialogue"),
        "3": ("satirical", "Comedic with biting satire and humor"),
        "4": ("epic", "Grand, mythic style with elevated language")
    }
    
    # If style was explicitly provided via CLI, use it
    if style_arg and style_arg != "choose":
        return style_arg
    
    # Interactive selection
    print("\n🎨 Choose output style:")
    print("-" * 40)
    for key, (name, desc) in STYLES.items():
        print(f"  {key}. {name.capitalize():12} - {desc}")
    print("-" * 40)
    
    while True:
        choice = input("Enter choice (1-4) [default: 1]: ").strip() or "1"
        if choice in STYLES:
            selected_style = STYLES[choice][0]
            print(f"✓ Selected: {selected_style.capitalize()}")
            return selected_style
        print("Invalid choice. Please enter 1, 2, 3, or 4.")


# ============================================================================
# STEP 4: SAVE THE RESULTS
# ============================================================================
def save_results(results, output_dir):
    """
    Save two files with unique timestamps:
    1. reimagined_story_TIMESTAMP.md - The final story
    2. transformation_log_TIMESTAMP.json - How characters/plot were mapped (for debugging)
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate unique timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a safe filename from the new title
    safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in results['map'].new_title)
    safe_title = safe_title.replace(" ", "_")[:30]  # Limit length
    
    # Save the story as Markdown
    story_filename = f"{safe_title}_{timestamp}.md"
    story_path = os.path.join(output_dir, story_filename)
    with open(story_path, "w", encoding="utf-8") as f:
        f.write(f"# {results['map'].new_title}\n\n")
        f.write(f"*Style: {results.get('style', 'narrative').capitalize()}*\n\n")
        f.write("---\n\n")
        f.write(results["story"])
    
    # Save the transformation log as JSON
    log_filename = f"{safe_title}_{timestamp}_log.json"
    log_path = os.path.join(output_dir, log_filename)
    with open(log_path, "w", encoding="utf-8") as f:
        log_data = {
            "generated_at": datetime.now().isoformat(),
            "original_contract": results["contract"].model_dump(),
            "context_map": results["map"].model_dump(),
            "style_used": results.get("style", "narrative")
        }
        json.dump(log_data, f, indent=2)
    
    print(f"\n✅ Success!")
    print(f"   Story saved to: {story_path}")
    print(f"   Log saved to:   {log_path}")


# ============================================================================
# MAIN FUNCTION - Orchestrates everything
# ============================================================================
def main():
    """
    Main function that runs when you execute: python run.py
    
    Flow:
    1. Parse command line arguments
    2. Get API key
    3. Load source story
    4. Run the 3-stage transformation pipeline
    5. Save results
    """
    
    # --- Parse Command Line Arguments ---
    parser = argparse.ArgumentParser(description="AI Story Transformer")
    parser.add_argument("--source", default="Cinderella", 
                        help="Story file path, 'Cinderella', or raw text")
    parser.add_argument("--target", default="Indian Education System", 
                        help="Target universe (e.g., 'Star Wars', 'Cyberpunk')")
    parser.add_argument("--output_dir", default="output", 
                        help="Folder to save results")
    parser.add_argument("--style", default="choose",
                        choices=["narrative", "screenplay", "satirical", "epic", "choose"],
                        help="Output style (or 'choose' for interactive selection)")
    parser.add_argument("--api_key", 
                        help="Groq API Key (optional if set in environment)")
    
    args = parser.parse_args()
    
    # --- Step 1: Get API Key ---
    api_key = get_api_key(args)
    
    # --- Step 2: Load Source Story ---
    source_text = load_source_story(args.source)
    
    # --- Step 3: Let User Choose Style ---
    style = choose_style(args.style)
    
    # --- Step 4: Create Transformer & Run Pipeline ---
    try:
        transformer = StoryTransformer(api_key=api_key)
        results = transformer.run_pipeline(source_text, args.target, style=style)
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        sys.exit(1)
    
    # --- Step 5: Save Results ---
    save_results(results, args.output_dir)


# ============================================================================
# ENTRY POINT - This runs when you execute the script
# ============================================================================
if __name__ == "__main__":
    main()
