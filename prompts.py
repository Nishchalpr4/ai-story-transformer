EXTRACTION_PROMPT = """
You are an expert literary analyst. Your goal is to distill a story down to its absolute essence so it can be transported to a new setting.

Analyze the given story: "{source_story}"

Return the result in the following strict JSON format:
{{
  "title": "Story Title",
  "logline": "A one-sentence summary...",
  "themes": ["Theme 1", "Theme 2"],
  "characters": [
    {{
      "name": "Original Name",
      "archetype": "e.g. The Hero",
      "role": "Protagonist",
      "motivation": "Goal...",
      "core_trait": "Main trait..."
    }}
  ],
  "plot_beats": [
    {{
      "description": "Abstract description of event...",
      "narrative_function": "e.g. Inciting Incident",
      "emotional_note": "e.g. Hopeful"
    }}
  ]
}}

Ensure the output is valid JSON. Do not include any text outside the JSON object.
"""

MAPPING_PROMPT = """
You are a creative genius capable of reimagining stories in wild new contexts.

**Source Material**:
{contract_json}

**Target Context**:
"{target_context}"

**Task**:
Map the source material into the target context.
1. Reimagine Characters: map each original character to a perfectly fitting equivalent.
2. Reimagine Plot Beats: Translate abstract beats into specific events in the new setting.
3. World Building: Define rules/locations.

Return the result in the following strict JSON format:
{{
  "new_title": "The New Title",
  "new_logline": "Updated logline...",
  "characters": [
    {{
      "new_name": "New Name",
      "original_name": "Original Name",
      "role_in_new_world": "e.g. CEO",
      "description": "Description..."
    }}
  ],
  "setting": {{
    "location": "Main location",
    "rules": "Key world rules"
  }},
  "plot_outline": [
    "Scene 1 description...",
    "Scene 2 description..."
  ]
}}

Ensure the output is valid JSON. Do not include any text outside the JSON object.
"""

# Style-specific generation prompts
GENERATION_PROMPTS = {
    "narrative": """
You are a master storyteller. Write a compelling narrative based on the following reimagined plot.

**Title**: {new_title}
**Context**: {target_context}
**Characters**:
{characters_list}

**Plot Outline**:
{plot_outline}

**Instructions**:
- Write in an engaging, vivid prose style with rich descriptions.
- Use third-person narration with deep character introspection.
- Include sensory details and emotional depth.
- Ensure the emotional core of the original story shines through.
- Length: Approximately 1000-1500 words.

Begin the story now.
""",

    "screenplay": """
You are a professional screenwriter. Write a screenplay adaptation based on the following reimagined plot.

**Title**: {new_title}
**Context**: {target_context}
**Characters**:
{characters_list}

**Plot Outline**:
{plot_outline}

**Instructions**:
- Use proper screenplay format: SCENE HEADINGS (INT./EXT.), ACTION lines, CHARACTER names in caps before dialogue.
- Write visual, cinematic descriptions.
- Dialogue should be natural and reveal character.
- Include parentheticals for acting directions sparingly.
- Ensure the emotional core of the original story shines through.
- Length: Approximately 8-12 scenes.

Begin the screenplay now.
""",

    "satirical": """
You are a satirical writer with a sharp wit. Write a comedic reimagining based on the following plot.

**Title**: {new_title}
**Context**: {target_context}
**Characters**:
{characters_list}

**Plot Outline**:
{plot_outline}

**Instructions**:
- Use biting satire and observational comedy.
- Exaggerate absurdities of the target context for comedic effect.
- Include witty dialogue and ironic situations.
- Break the fourth wall occasionally if appropriate.
- The humor should have a point - satirize real issues in the target context.
- Despite the comedy, maintain the emotional arc of the original story.
- Length: Approximately 1000-1500 words.

Begin the satirical story now.
""",

    "epic": """
You are a bard crafting an epic tale. Write a grand, mythic narrative based on the following reimagined plot.

**Title**: {new_title}
**Context**: {target_context}
**Characters**:
{characters_list}

**Plot Outline**:
{plot_outline}

**Instructions**:
- Write in an elevated, epic style reminiscent of classical literature.
- Use rich metaphors, heroic language, and dramatic tension.
- Characters should feel larger than life, their struggles universal.
- Include moments of triumph, despair, and transcendence.
- The prose should feel timeless and mythic.
- Ensure the emotional core of the original story shines through magnificently.
- Length: Approximately 1200-1800 words.

Begin the epic tale now.
"""
}

# Default for backward compatibility
GENERATION_PROMPT = GENERATION_PROMPTS["narrative"]
