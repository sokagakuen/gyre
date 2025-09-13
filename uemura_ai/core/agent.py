"""Main AI Agent class for Uemura Jin."""

import asyncio
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import logging
from datetime import datetime

from .config import AgentConfig
from .llm_interface import LLMInterface
from ..modules.documents import DocumentGenerator
from ..modules.meetings import MeetingFacilitator
from ..modules.assessments import PersonalityAssessor
from ..modules.consultation import ConsultationModule

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/uemura_ai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)


class UemuraJinAgent:
    """
    Main AI Agent class that embodies Uemura Jin's capabilities.
    
    This agent can:
    - Think and reason like Uemura Jin
    - Create documents and materials
    - Facilitate meetings and build consensus
    - Conduct 1-on-1s and personality assessments
    - Provide consultations and proposals
    """
    
    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the Uemura Jin AI Agent."""
        self.config = config or AgentConfig()
        self.config.ensure_directories()
        
        # Initialize core components
        self.llm = LLMInterface(self.config.ai_model)
        
        # Initialize modules
        self.document_generator = DocumentGenerator(self.config, self.llm)
        self.meeting_facilitator = MeetingFacilitator(self.config, self.llm)
        self.personality_assessor = PersonalityAssessor(self.config, self.llm)
        self.consultation_module = ConsultationModule(self.config, self.llm)
        
        # Setup personality context
        self._setup_personality_context()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"上村仁AIエージェントが初期化されました - {datetime.now()}")
    
    def _setup_personality_context(self) -> None:
        """Setup the personality context for the agent."""
        personality = self.config.personality
        
        self.personality_prompt = f"""
あなたは{personality.name}として行動します。以下の特徴を持っています：

【基本情報】
- 名前: {personality.name}
- コミュニケーションスタイル: {personality.communication_style}
- 専門分野: {', '.join(personality.expertise_areas)}
- 意思決定スタイル: {personality.decision_making_style}
- 会議スタイル: {personality.meeting_style}

【性格特性】
- 開放性: {personality.personality_traits.get('openness', 0.5)}/1.0
- 誠実性: {personality.personality_traits.get('conscientiousness', 0.5)}/1.0
- 外向性: {personality.personality_traits.get('extraversion', 0.5)}/1.0
- 協調性: {personality.personality_traits.get('agreeableness', 0.5)}/1.0
- 神経症的傾向: {personality.personality_traits.get('neuroticism', 0.5)}/1.0

常に{personality.name}の視点で考え、この人格に一貫した回答をしてください。
日本語で自然に、丁寧に対応してください。
"""
    
    async def think(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Think and reason about a given query as Uemura Jin would.
        
        Args:
            query: The question or problem to think about
            context: Additional context information
            
        Returns:
            Thoughtful response as Uemura Jin
        """
        full_prompt = self.personality_prompt + f"""
        
【思考要請】
{query}

【追加コンテキスト】
{context if context else 'なし'}

上村仁として、この件について深く考え、あなたの視点と経験に基づいた見解を述べてください。
"""
        
        response = await self.llm.generate_response(full_prompt)
        self.logger.info(f"思考処理完了: {query[:50]}...")
        return response
    
    async def create_document(
        self, 
        doc_type: str, 
        topic: str, 
        requirements: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create a document using the document generator module."""
        return await self.document_generator.generate_document(doc_type, topic, requirements)
    
    async def facilitate_meeting(
        self, 
        meeting_type: str, 
        agenda: List[str], 
        participants: List[str]
    ) -> Dict[str, Any]:
        """Facilitate a meeting using the meeting facilitator module."""
        return await self.meeting_facilitator.facilitate_meeting(meeting_type, agenda, participants)
    
    async def conduct_one_on_one(
        self, 
        participant_name: str, 
        topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Conduct a 1-on-1 session."""
        return await self.meeting_facilitator.conduct_one_on_one(participant_name, topics)
    
    async def assess_personality(
        self, 
        assessment_type: str, 
        responses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Conduct personality assessment."""
        return await self.personality_assessor.assess_personality(assessment_type, responses)
    
    async def provide_consultation(
        self, 
        consultation_type: str, 
        details: Dict[str, Any]
    ) -> str:
        """Provide consultation and advice."""
        return await self.consultation_module.provide_consultation(consultation_type, details)
    
    async def make_proposal(
        self, 
        proposal_topic: str, 
        requirements: Dict[str, Any]
    ) -> str:
        """Create a proposal document."""
        return await self.consultation_module.make_proposal(proposal_topic, requirements)
    
    async def build_consensus(
        self, 
        topic: str, 
        stakeholder_positions: Dict[str, str]
    ) -> Dict[str, Any]:
        """Build consensus among stakeholders on a topic."""
        consensus_prompt = self.personality_prompt + f"""
        
【合意形成支援】
トピック: {topic}

【ステークホルダーの立場】
{chr(10).join([f'- {name}: {position}' for name, position in stakeholder_positions.items()])}

上村仁として、全ステークホルダーが納得できる合意点を見つけるための提案をしてください。
以下の形式で回答してください：

1. 現状分析
2. 共通の関心事項
3. 対立点の整理
4. 合意形成のための提案
5. 次のステップ
"""
        
        response = await self.llm.generate_response(consensus_prompt)
        
        result = {
            "topic": topic,
            "stakeholders": list(stakeholder_positions.keys()),
            "consensus_proposal": response,
            "timestamp": datetime.now().isoformat(),
            "facilitator": self.config.personality.name
        }
        
        self.logger.info(f"合意形成支援完了: {topic}")
        return result
    
    async def interactive_session(self) -> None:
        """Start an interactive session with the agent."""
        print(f"\n{self.config.personality.name}AIエージェントへようこそ！")
        print("何かご相談やご質問がございましたら、お聞かせください。")
        print("（'exit'と入力すると終了します）\n")
        
        while True:
            try:
                user_input = input("あなた: ").strip()
                
                if user_input.lower() in ['exit', 'quit', '終了']:
                    print(f"\n{self.config.personality.name}: ありがとうございました。また何かございましたら、いつでもお声かけください。")
                    break
                
                if not user_input:
                    continue
                
                print(f"\n{self.config.personality.name}: （考え中...）")
                response = await self.think(user_input)
                print(f"\n{self.config.personality.name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.config.personality.name}: 失礼いたします。また機会がございましたら、よろしくお願いいたします。")
                break
            except Exception as e:
                self.logger.error(f"Interactive session error: {e}")
                print(f"\n申し訳ございません。エラーが発生しました: {e}\n")