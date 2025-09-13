"""
上村仁 AI Agent
AI agent system to replace/assist Uemura Jin with comprehensive capabilities.
"""

__version__ = "0.1.0"
__author__ = "AI Development Team"
__email__ = "dev@sokagakuen.com"

from .core.agent import UemuraJinAgent
from .core.config import AgentConfig

__all__ = ["UemuraJinAgent", "AgentConfig"]