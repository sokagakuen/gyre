"""Configuration management for the Uemura Jin AI Agent."""

import os
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PersonalityConfig(BaseModel):
    """Configuration for agent personality traits."""
    
    name: str = "上村仁"
    language: str = "ja"
    communication_style: str = "polite_formal"
    expertise_areas: List[str] = ["management", "strategy", "team_leadership"]
    decision_making_style: str = "analytical_collaborative"
    meeting_style: str = "facilitative_consensus_building"
    personality_traits: Dict[str, float] = {
        "openness": 0.8,
        "conscientiousness": 0.9,
        "extraversion": 0.7,
        "agreeableness": 0.8,
        "neuroticism": 0.2
    }


class AIModelConfig(BaseModel):
    """Configuration for AI model settings."""
    
    openai_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY"))
    anthropic_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))
    default_model: str = Field(default_factory=lambda: os.getenv("DEFAULT_MODEL", "gpt-4"))
    temperature: float = Field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = Field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "2000")))


class AgentConfig(BaseModel):
    """Main configuration for the Uemura Jin AI Agent."""
    
    personality: PersonalityConfig = Field(default_factory=PersonalityConfig)
    ai_model: AIModelConfig = Field(default_factory=AIModelConfig)
    
    # Directory configurations
    template_dir: Path = Path("templates")
    output_dir: Path = Path("output")
    config_dir: Path = Path("config")
    
    # Module-specific configurations
    document_templates: Path = Field(default_factory=lambda: Path("templates/documents"))
    meeting_templates: Path = Field(default_factory=lambda: Path("templates/meetings"))
    assessment_templates: Path = Field(default_factory=lambda: Path("templates/assessments"))
    
    # Meeting configuration
    default_meeting_duration: int = Field(default_factory=lambda: int(os.getenv("DEFAULT_MEETING_DURATION", "60")))
    
    # Assessment configuration
    personality_models: List[str] = Field(default_factory=lambda: os.getenv("PERSONALITY_MODELS", "mbti,big5,disc").split(","))
    
    @classmethod
    def from_file(cls, config_path: Path) -> "AgentConfig":
        """Load configuration from YAML file."""
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
            return cls(**config_data)
        return cls()
    
    def save_to_file(self, config_path: Path) -> None:
        """Save configuration to YAML file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(self.model_dump(), f, default_flow_style=False, allow_unicode=True)
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.template_dir,
            self.output_dir,
            self.config_dir,
            self.document_templates,
            self.meeting_templates,
            self.assessment_templates,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)