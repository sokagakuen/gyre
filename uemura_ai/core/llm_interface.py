"""Language Model Interface for the Uemura Jin AI Agent."""

import asyncio
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .config import AIModelConfig


class LLMInterface:
    """Interface for Language Model interactions."""
    
    def __init__(self, config: AIModelConfig):
        """Initialize the LLM interface."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize available clients
        self.openai_client = None
        self.anthropic_client = None
        
        if OPENAI_AVAILABLE and config.openai_api_key:
            self.openai_client = openai.AsyncOpenAI(api_key=config.openai_api_key)
        
        if ANTHROPIC_AVAILABLE and config.anthropic_api_key:
            self.anthropic_client = anthropic.AsyncAnthropic(api_key=config.anthropic_api_key)
    
    async def generate_response(
        self, 
        prompt: str, 
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response using the configured language model.
        
        Args:
            prompt: The input prompt
            model: Model to use (defaults to config.default_model)
            temperature: Temperature for generation (defaults to config.temperature)
            max_tokens: Maximum tokens (defaults to config.max_tokens)
            
        Returns:
            Generated response text
        """
        model = model or self.config.default_model
        temperature = temperature or self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        try:
            if model.startswith("gpt") and self.openai_client:
                return await self._generate_openai_response(prompt, model, temperature, max_tokens)
            elif model.startswith("claude") and self.anthropic_client:
                return await self._generate_anthropic_response(prompt, model, temperature, max_tokens)
            else:
                # Fallback to mock response for development/testing
                return await self._generate_mock_response(prompt)
                
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return f"申し訳ございません。システムエラーが発生しました: {str(e)}"
    
    async def _generate_openai_response(
        self, 
        prompt: str, 
        model: str, 
        temperature: float, 
        max_tokens: int
    ) -> str:
        """Generate response using OpenAI API."""
        try:
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "あなたは上村仁として行動する知的なアシスタントです。日本語で自然に、丁寧に対応してください。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _generate_anthropic_response(
        self, 
        prompt: str, 
        model: str, 
        temperature: float, 
        max_tokens: int
    ) -> str:
        """Generate response using Anthropic API."""
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            self.logger.error(f"Anthropic API error: {e}")
            raise
    
    async def _generate_mock_response(self, prompt: str) -> str:
        """Generate a mock response for development/testing."""
        await asyncio.sleep(1)  # Simulate API delay
        
        # Simple mock responses based on prompt content
        if "文書" in prompt or "ドキュメント" in prompt:
            return """承知いたしました。ご指定の文書を作成いたします。

【構成案】
1. 概要・目的
2. 背景・現状分析
3. 具体的な提案・内容
4. 実施計画・スケジュール
5. 期待される効果・成果

詳細について、さらにご要望がございましたらお聞かせください。"""
        
        elif "会議" in prompt or "ミーティング" in prompt:
            return """会議の進行について承知いたしました。

【進行方針】
1. アジェンダの確認と時間配分
2. 各議題について建設的な議論を促進
3. 全参加者の意見を聴取
4. 合意形成に向けた調整
5. 明確な次のアクションを決定

参加者の皆様が有意義な時間を過ごせるよう、効果的に進行させていただきます。"""
        
        elif "評価" in prompt or "アセスメント" in prompt:
            return """パーソナリティ評価について承知いたします。

【評価の観点】
- コミュニケーションスタイル
- 意思決定の傾向
- チームでの役割適性
- 強みと成長機会
- 適切な業務環境

客観的かつ建設的な評価を心がけ、個人の成長に資する形でフィードバックいたします。"""
        
        elif "相談" in prompt or "提案" in prompt:
            return """ご相談いただき、ありがとうございます。

【分析の視点】
- 現状の整理と課題の明確化
- 複数の選択肢の検討
- リスクと機会の評価
- 実現可能性の検証
- 長期的な影響の考慮

皆様の状況を踏まえた、実践的で建設的な提案をさせていただきます。詳細についてお聞かせください。"""
        
        else:
            return f"""承知いたしました。{datetime.now().strftime('%Y年%m月%d日')}現在の上村仁として、ご質問について深く考えさせていただきます。

私の経験と知見を活かして、皆様のお役に立てるよう努めます。さらに詳しい状況やご要望について、お聞かせいただけますでしょうか。

（注：これは開発用のモック応答です。実際の運用では適切なAI APIキーを設定してください。）"""
    
    async def generate_structured_response(
        self, 
        prompt: str, 
        structure: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Generate a structured response with specific sections.
        
        Args:
            prompt: The input prompt
            structure: Dictionary defining the required sections
            
        Returns:
            Dictionary with structured response
        """
        structured_prompt = prompt + "\n\n以下の構造で回答してください：\n"
        for key, description in structure.items():
            structured_prompt += f"【{key}】{description}\n"
        
        response = await self.generate_response(structured_prompt)
        
        # Parse the structured response (simple implementation)
        result = {}
        current_section = None
        current_content = []
        
        for line in response.split('\n'):
            line = line.strip()
            if line.startswith('【') and line.endswith('】'):
                if current_section:
                    result[current_section] = '\n'.join(current_content).strip()
                current_section = line[1:-1]
                current_content = []
            else:
                current_content.append(line)
        
        if current_section:
            result[current_section] = '\n'.join(current_content).strip()
        
        return result