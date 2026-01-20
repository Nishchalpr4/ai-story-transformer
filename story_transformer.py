"""
Story Transformer - Core Pipeline
==================================
A 3-stage AI pipeline that transforms stories into new cultural contexts.

Pipeline:
    1. Extract  - Pull out archetypes, themes, and plot structure
    2. Map      - Translate elements to the target setting
    3. Generate - Write the final story in chosen style
"""

import json
import time
import logging
from pydantic import BaseModel, ValidationError
from typing import List
from groq import Groq
from prompts import EXTRACTION_PROMPT, MAPPING_PROMPT, GENERATION_PROMPTS

logger = logging.getLogger(__name__)


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class TransformationError(Exception):
    """Raised when story transformation fails."""
    pass


# ============================================================================
# DATA MODELS (Pydantic ensures LLM returns valid structured data)
# ============================================================================

class Character(BaseModel):
    """Character extracted from original story."""
    name: str
    archetype: str       # e.g., Underdog, Mentor, Villain
    role: str            # Protagonist, Antagonist, Support
    motivation: str
    core_trait: str


class PlotBeat(BaseModel):
    """A key story moment, described abstractly."""
    description: str
    narrative_function: str   # Setup, Conflict, Climax, Resolution
    emotional_note: str       # Hopeful, Tense, Triumphant


class StoryEssence(BaseModel):
    """The 'DNA' of the original story - setting-independent."""
    title: str
    logline: str
    themes: List[str]
    characters: List[Character]
    plot_beats: List[PlotBeat]


class NewCharacter(BaseModel):
    """Character adapted to the new setting."""
    new_name: str
    original_name: str
    role_in_new_world: str
    description: str


class StoryMap(BaseModel):
    """Complete blueprint for the story in the new setting."""
    new_title: str
    new_logline: str
    characters: List[NewCharacter]
    setting: dict
    plot_outline: List[str]


# ============================================================================
# TRANSFORMER
# ============================================================================

class StoryTransformer:
    """
    Transforms stories using a 3-stage prompt chain.
    
    Each stage builds on the previous:
        Story Text → [Extract] → Essence → [Map] → Blueprint → [Generate] → Final Story
    """
    
    MODEL = "llama-3.3-70b-versatile"
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds
    
    def __init__(self, api_key: str):
        if not api_key:
            raise TransformationError("API key is required")
        self.client = Groq(api_key=api_key)
    
    def _call_llm(self, prompt: str, json_mode: bool = False) -> str:
        """Send prompt to LLM with retry logic."""
        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(
                    model=self.MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"} if json_mode else None,
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.warning(f"API call failed (attempt {attempt + 1}): {e}")
                if attempt < self.MAX_RETRIES - 1:
                    time.sleep(self.RETRY_DELAY)
                else:
                    raise TransformationError(f"API call failed after {self.MAX_RETRIES} attempts: {e}")
    
    def extract(self, story: str) -> StoryEssence:
        """Stage 1: Extract abstract story elements."""
        if not story or len(story.strip()) < 50:
            raise TransformationError("Story text is too short or empty")
            
        print("\n[Stage 1] Extracting story essence...")
        
        prompt = EXTRACTION_PROMPT.format(source_story=story)
        response = self._call_llm(prompt, json_mode=True)
        
        try:
            essence = StoryEssence(**json.loads(response))
        except (json.JSONDecodeError, ValidationError) as e:
            raise TransformationError(f"Failed to parse extraction response: {e}")
        
        print(f"  → {len(essence.characters)} characters, {len(essence.plot_beats)} plot beats")
        logger.info(f"Extracted: {essence.title}")
        return essence
    
    def map_to_setting(self, essence: StoryEssence, target: str) -> StoryMap:
        """Stage 2: Map story elements to target setting."""
        if not target or len(target.strip()) < 3:
            raise TransformationError("Target setting is required")
            
        print(f"\n[Stage 2] Mapping to '{target}'...")
        
        prompt = MAPPING_PROMPT.format(
            contract_json=essence.model_dump_json(indent=2),
            target_context=target
        )
        response = self._call_llm(prompt, json_mode=True)
        
        try:
            story_map = StoryMap(**json.loads(response))
        except (json.JSONDecodeError, ValidationError) as e:
            raise TransformationError(f"Failed to parse mapping response: {e}")
        
        print(f"  → New title: {story_map.new_title}")
        logger.info(f"Mapped to: {story_map.new_title}")
        return story_map
    
    def generate(self, story_map: StoryMap, target: str, style: str) -> str:
        """Stage 3: Generate final story."""
        valid_styles = ["narrative", "screenplay", "satirical", "epic"]
        if style not in valid_styles:
            raise TransformationError(f"Invalid style. Choose from: {valid_styles}")
            
        print(f"\n[Stage 3] Generating {style} story...")
        
        # Format data for the prompt
        characters = "\n".join([
            f"- {c.new_name}: {c.description}" 
            for c in story_map.characters
        ])
        plot = "\n".join(story_map.plot_outline)
        
        prompt = GENERATION_PROMPTS[style].format(
            new_title=story_map.new_title,
            target_context=target,
            characters_list=characters,
            plot_outline=plot
        )
        
        final_story = self._call_llm(prompt)
        word_count = len(final_story.split())
        print(f"  → Generated {word_count} words")
        logger.info(f"Generated {word_count} word {style} story")
        return final_story
    
    def transform(self, story: str, target: str = "Indian Education System", style: str = "narrative") -> dict:
        """
        Run the complete 3-stage transformation pipeline.
        
        Args:
            story: Original story text
            target: Target cultural context
            style: Output style (narrative, screenplay, satirical, epic)
            
        Returns:
            Dict with 'story', 'contract' (essence), and 'map' (blueprint)
        """
        # Stage 1: Extract
        essence = self.extract(story)
        
        # Stage 2: Map
        story_map = self.map_to_setting(essence, target)
        
        # Stage 3: Generate
        final_story = self.generate(story_map, target, style)
        
        return {
            "story": final_story,
            "contract": essence,
            "map": story_map,
            "style": style
        }