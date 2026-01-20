"""
Prompts for Story Transformer Pipeline
=======================================
Each prompt is designed for a specific stage of the transformation.
"""

# ============================================================================
# STAGE 1: EXTRACTION
# Purpose: Pull out the abstract "DNA" of the story (setting-independent)
# ============================================================================

EXTRACTION_PROMPT = """
Analyze this story and extract its core elements.

STORY:
"{source_story}"

Return a JSON object with:
{{
  "title": "story title",
  "logline": "one sentence summary",
  "themes": ["theme1", "theme2"],
  "characters": [
    {{
      "name": "character name",
      "archetype": "Underdog/Mentor/Villain/etc",
      "role": "Protagonist/Antagonist/Support",
      "motivation": "what drives them",
      "core_trait": "defining personality trait"
    }}
  ],
  "plot_beats": [
    {{
      "description": "what happens (abstract, not setting-specific)",
      "narrative_function": "Setup/Conflict/Climax/Resolution",
      "emotional_note": "emotional tone of this moment"
    }}
  ]
}}

Return ONLY valid JSON, no other text.
"""


# ============================================================================
# STAGE 2: MAPPING
# Purpose: Translate abstract elements into the target setting
# ============================================================================

MAPPING_PROMPT = """
Reimagine this story in a completely new setting.

ORIGINAL STORY ELEMENTS:
{contract_json}

TARGET SETTING: "{target_context}"

Create new character names and roles that fit the target setting.
Translate each plot beat into a concrete scene in the new world.

Return a JSON object:
{{
  "new_title": "title for the new version",
  "new_logline": "updated one-line summary",
  "characters": [
    {{
      "new_name": "name in new setting",
      "original_name": "original name",
      "role_in_new_world": "their role in this setting",
      "description": "brief character description"
    }}
  ],
  "setting": {{
    "location": "primary location",
    "rules": "how this world works"
  }},
  "plot_outline": [
    "Scene 1: description",
    "Scene 2: description"
  ]
}}

Return ONLY valid JSON, no other text.
"""


# ============================================================================
# STAGE 3: GENERATION
# Purpose: Write the final story in the chosen style
# ============================================================================

GENERATION_PROMPTS = {
    
    "narrative": """
Write a complete story based on this outline.

TITLE: {new_title}
SETTING: {target_context}

CHARACTERS:
{characters_list}

PLOT OUTLINE:
{plot_outline}

Requirements:
- Third person narration
- Include character thoughts and emotions
- Vivid descriptions of the setting
- 1000-1500 words
""",

    "screenplay": """
Write a screenplay based on this outline.

TITLE: {new_title}
SETTING: {target_context}

CHARACTERS:
{characters_list}

PLOT OUTLINE:
{plot_outline}

Requirements:
- Proper screenplay format (INT./EXT. headings)
- Character names in CAPS before dialogue
- Action lines and visual descriptions
- 8-12 scenes
""",

    "satirical": """
Write a satirical comedy based on this outline.

TITLE: {new_title}
SETTING: {target_context}

CHARACTERS:
{characters_list}

PLOT OUTLINE:
{plot_outline}

Requirements:
- Humorous and ironic tone
- Exaggerate the absurdities of the setting
- Witty dialogue
- Keep the emotional arc intact
- 1000-1500 words
""",

    "epic": """
Write an epic tale based on this outline.

TITLE: {new_title}
SETTING: {target_context}

CHARACTERS:
{characters_list}

PLOT OUTLINE:
{plot_outline}

Requirements:
- Grand, mythic language
- Characters feel larger than life
- Rich metaphors and imagery
- Moments of triumph and despair
- 1200-1800 words
"""
}