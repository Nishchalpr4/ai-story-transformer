import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field
from groq import Groq
from prompts import EXTRACTION_PROMPT, MAPPING_PROMPT, GENERATION_PROMPTS

# --- Data Models (The "Transformation Contract") ---

class Character(BaseModel):
    name: str = Field(..., description="Original name of the character")
    archetype: str = Field(..., description="Character archetype (e.g., Hero, Villian)")
    role: str = Field(..., description="Role in the story")
    motivation: str = Field(..., description="Primary motivation")
    core_trait: str = Field(..., description="Defining personality trait")

class PlotBeat(BaseModel):
    description: str = Field(..., description="Abstract description of the event")
    narrative_function: str = Field(..., description="Why this scene exists")
    emotional_note: str = Field(..., description="Emotional tone")

class TransformationContract(BaseModel):
    title: Optional[str] = "Unknown"
    logline: str
    themes: List[str]
    characters: List[Character]
    plot_beats: List[PlotBeat]

class ReimaginedCharacter(BaseModel):
    new_name: str
    original_name: str
    role_in_new_world: str
    description: str

class ReimaginedStoryMap(BaseModel):
    new_title: str
    new_logline: str
    characters: List[ReimaginedCharacter]
    setting: dict
    plot_outline: List[str]

# --- Core Logic ---

class StoryTransformer:
    def __init__(self, api_key: str, model_name="llama-3.3-70b-versatile"):
        if not api_key:
            raise ValueError("Groq API Key is required.")
        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def _call_llm(self, prompt: str, json_mode: bool = False) -> str:
        """Helper to call Groq API."""
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.model_name,
            response_format={"type": "json_object"} if json_mode else None,
        )
        return chat_completion.choices[0].message.content

    def extract_contract(self, source_story: str) -> TransformationContract:
        """Step 1: Extract the essence of the story."""
        prompt = EXTRACTION_PROMPT.format(source_story=source_story) + "\n\nIMPORTANT: Return ONLY valid JSON."
        
        response_text = self._call_llm(prompt, json_mode=True)
        
        try:
            data = json.loads(response_text)
            return TransformationContract(**data)
        except Exception as e:
            print(f"Error parsing extraction response: {e}")
            print(f"Raw response: {response_text}")
            raise

    def map_to_context(self, contract: TransformationContract, target_context: str) -> ReimaginedStoryMap:
        """Step 2: Map the essence to the new world."""
        contract_json = contract.model_dump_json(indent=2)
        prompt = MAPPING_PROMPT.format(contract_json=contract_json, target_context=target_context) + "\n\nIMPORTANT: Return ONLY valid JSON."
        
        response_text = self._call_llm(prompt, json_mode=True)
        
        try:
            data = json.loads(response_text)
            return ReimaginedStoryMap(**data)
        except Exception as e:
            print(f"Error parsing mapping response: {e}")
            print(f"Raw response: {response_text}")
            raise

    def generate_story(self, story_map: ReimaginedStoryMap, target_context: str, style: str = "narrative") -> str:
        """Step 3: Write the full story in the specified style."""
        chars_desc = "\n".join([f"- {c.new_name} ({c.role_in_new_world}): {c.description}" for c in story_map.characters])
        plot_desc = "\n".join([f"{i+1}. {beat}" for i, beat in enumerate(story_map.plot_outline)])
        
        # Select the appropriate prompt based on style
        generation_prompt = GENERATION_PROMPTS.get(style, GENERATION_PROMPTS["narrative"])
        
        prompt = generation_prompt.format(
            new_title=story_map.new_title,
            target_context=target_context,
            characters_list=chars_desc,
            plot_outline=plot_desc
        )
        
        return self._call_llm(prompt, json_mode=False)

    def run_pipeline(self, source_story_text: str, target_context: str, style: str = "narrative") -> dict:
        print(f"--- 1. Extracting Essence from source... ---")
        contract = self.extract_contract(source_story_text)
        print(f"Extracted: {contract.logline}")
        
        print(f"\n--- 2. Mapping to '{target_context}'... ---")
        story_map = self.map_to_context(contract, target_context)
        print(f"New Title: {story_map.new_title}")
        
        print(f"\n--- 3. Generating Story (style: {style})... ---")
        full_story = self.generate_story(story_map, target_context, style)
        
        return {
            "contract": contract,
            "map": story_map,
            "story": full_story,
            "style": style
        }
