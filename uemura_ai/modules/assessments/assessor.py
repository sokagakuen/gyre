"""Personality assessment functionality."""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import logging

from ...core.config import AgentConfig
from ...core.llm_interface import LLMInterface


class PersonalityAssessor:
    """Conduct personality assessments and provide insights."""
    
    def __init__(self, config: AgentConfig, llm: LLMInterface):
        """Initialize the personality assessor."""
        self.config = config
        self.llm = llm
        self.logger = logging.getLogger(__name__)
        
        # Assessment frameworks
        self.assessment_frameworks = {
            "mbti": self._mbti_assessment,
            "big5": self._big5_assessment,
            "disc": self._disc_assessment,
            "strengths": self._strengths_assessment
        }
    
    async def assess_personality(
        self, 
        assessment_type: str, 
        responses: Dict[str, Any],
        participant_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Conduct personality assessment based on responses.
        
        Args:
            assessment_type: Type of assessment (mbti, big5, disc, strengths)
            responses: Assessment responses or behavioral observations
            participant_name: Name of the person being assessed
            
        Returns:
            Assessment results and insights
        """
        if assessment_type not in self.assessment_frameworks:
            raise ValueError(f"Unsupported assessment type: {assessment_type}")
        
        assessment_func = self.assessment_frameworks[assessment_type]
        result = await assessment_func(responses, participant_name)
        
        # Add metadata
        result.update({
            "assessment_type": assessment_type,
            "participant": participant_name or "匿名",
            "assessor": self.config.personality.name,
            "timestamp": datetime.now().isoformat()
        })
        
        # Save assessment result
        await self._save_assessment_result(result, assessment_type, participant_name)
        
        self.logger.info(f"Assessment completed: {assessment_type} for {participant_name or 'anonymous'}")
        return result
    
    async def _mbti_assessment(
        self, 
        responses: Dict[str, Any], 
        participant_name: Optional[str]
    ) -> Dict[str, Any]:
        """Conduct MBTI-style personality assessment."""
        
        mbti_prompt = f"""
以下の情報を基に、MBTI（16タイプ性格診断）の観点から性格分析を行ってください。

【対象者情報】
{f'名前: {participant_name}' if participant_name else '対象者: 匿名'}

【回答・観察データ】
{self._format_responses(responses)}

以下の形式で分析結果を提供してください：

【MBTI分析結果】
予想されるタイプ: [4文字のタイプ]

【各次元の分析】
- 外向性(E) vs 内向性(I): 
- 直感(N) vs 感覚(S): 
- 思考(T) vs 感情(F): 
- 判断(J) vs 知覚(P): 

【性格の特徴】
- 主な強み:
- 潜在的な課題:
- コミュニケーションスタイル:
- 意思決定の傾向:

【職場での特性】
- 適している役割:
- チームでの貢献:
- ストレス要因:
- 成長のためのアドバイス:

{self.config.personality.name}として、建設的で成長に資する分析を心がけてください。
"""
        
        analysis = await self.llm.generate_response(mbti_prompt)
        
        return {
            "framework": "MBTI",
            "analysis": analysis,
            "insights": await self._generate_insights(analysis, "MBTI")
        }
    
    async def _big5_assessment(
        self, 
        responses: Dict[str, Any], 
        participant_name: Optional[str]
    ) -> Dict[str, Any]:
        """Conduct Big Five personality assessment."""
        
        big5_prompt = f"""
以下の情報を基に、ビッグファイブ（Big Five）性格特性の観点から分析を行ってください。

【対象者情報】
{f'名前: {participant_name}' if participant_name else '対象者: 匿名'}

【回答・観察データ】
{self._format_responses(responses)}

以下の形式で分析結果を提供してください：

【ビッグファイブ分析結果】

【各特性の評価】（1-10のスケールで評価）
- 開放性（Openness）: [点数] - [説明]
- 誠実性（Conscientiousness）: [点数] - [説明]  
- 外向性（Extraversion）: [点数] - [説明]
- 協調性（Agreeableness）: [点数] - [説明]
- 神経症的傾向（Neuroticism）: [点数] - [説明]

【総合的な性格像】
- 性格の全体的な特徴:
- 行動パターンの傾向:
- 対人関係での特徴:

【実践的なアドバイス】
- 強みを活かす方法:
- 注意すべき点:
- 成長のための提案:

科学的根拠に基づき、{self.config.personality.name}として客観的な分析を提供してください。
"""
        
        analysis = await self.llm.generate_response(big5_prompt)
        
        return {
            "framework": "Big Five",
            "analysis": analysis,
            "insights": await self._generate_insights(analysis, "Big Five")
        }
    
    async def _disc_assessment(
        self, 
        responses: Dict[str, Any], 
        participant_name: Optional[str]
    ) -> Dict[str, Any]:
        """Conduct DISC behavioral assessment."""
        
        disc_prompt = f"""
以下の情報を基に、DISC行動特性の観点から分析を行ってください。

【対象者情報】
{f'名前: {participant_name}' if participant_name else '対象者: 匿名'}

【回答・観察データ】
{self._format_responses(responses)}

以下の形式で分析結果を提供してください：

【DISC分析結果】

【各特性の評価】（高・中・低で評価）
- 主導性（Dominance）: [レベル] - [行動の特徴]
- 影響性（Influence）: [レベル] - [行動の特徴]
- 安定性（Steadiness）: [レベル] - [行動の特徴]
- 慎重性（Conscientiousness）: [レベル] - [行動の特徴]

【主要な行動スタイル】
- 仕事への取り組み方:
- コミュニケーションの特徴:
- 意思決定のスタイル:
- ストレス下での行動:

【職場での活用】
- 適している業務:
- 効果的な動機づけ方法:
- 他のタイプとの協働方法:
- リーダーシップのスタイル:

{self.config.personality.name}として、実用的で行動に移しやすい分析を提供してください。
"""
        
        analysis = await self.llm.generate_response(disc_prompt)
        
        return {
            "framework": "DISC",
            "analysis": analysis,
            "insights": await self._generate_insights(analysis, "DISC") 
        }
    
    async def _strengths_assessment(
        self, 
        responses: Dict[str, Any], 
        participant_name: Optional[str]
    ) -> Dict[str, Any]:
        """Conduct strengths-based assessment."""
        
        strengths_prompt = f"""
以下の情報を基に、強みベースの観点から才能と能力を分析してください。

【対象者情報】
{f'名前: {participant_name}' if participant_name else '対象者: 匿名'}

【回答・観察データ】
{self._format_responses(responses)}

以下の形式で分析結果を提供してください：

【強み分析結果】

【主要な強み】（上位5つ）
1. [強み名]: [具体的な説明と発揮場面]
2. [強み名]: [具体的な説明と発揮場面]
3. [強み名]: [具体的な説明と発揮場面]
4. [強み名]: [具体的な説明と発揮場面]
5. [強み名]: [具体的な説明と発揮場面]

【強みの活用方法】
- 現在の役割での活かし方:
- キャリア発展への活用:
- チームへの貢献方法:

【成長のための提案】
- 強みをさらに伸ばす方法:
- 弱い分野の補完方法:
- 新しい挑戦の機会:

【実践的なアクションプラン】
- 今日からできること:
- 1ヶ月以内の目標:
- 長期的な発展方向:

{self.config.personality.name}として、前向きで実行可能な分析を心がけてください。
"""
        
        analysis = await self.llm.generate_response(strengths_prompt)
        
        return {
            "framework": "Strengths",
            "analysis": analysis,
            "insights": await self._generate_insights(analysis, "Strengths")
        }
    
    async def _generate_insights(self, analysis: str, framework: str) -> List[str]:
        """Generate key insights from the analysis."""
        
        insights_prompt = f"""
以下の{framework}分析結果から、重要な洞察を3-5個抽出してください。

【分析結果】
{analysis}

各洞察は以下の形式で：
- [洞察内容]（簡潔で実用的な形で）

{self.config.personality.name}として、行動に移しやすい洞察を提供してください。
"""
        
        insights_text = await self.llm.generate_response(insights_prompt)
        
        # Parse insights (simple implementation)
        insights = []
        for line in insights_text.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                insights.append(line[2:])
        
        return insights[:5]  # Limit to 5 insights
    
    def _format_responses(self, responses: Dict[str, Any]) -> str:
        """Format assessment responses for analysis."""
        if not responses:
            return "回答データが提供されていません。"
        
        formatted = []
        for key, value in responses.items():
            if isinstance(value, list):
                formatted.append(f"{key}: {', '.join(map(str, value))}")
            elif isinstance(value, dict):
                formatted.append(f"{key}: {json.dumps(value, ensure_ascii=False, indent=2)}")
            else:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)
    
    async def _save_assessment_result(
        self, 
        result: Dict[str, Any], 
        assessment_type: str, 
        participant_name: Optional[str]
    ) -> None:
        """Save assessment result to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        participant_id = participant_name.replace(" ", "_") if participant_name else "anonymous"
        filename = f"{assessment_type}_assessment_{participant_id}_{timestamp}.md"
        output_path = self.config.output_dir / "assessments" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Format as markdown
        content = f"""# {result['framework']} Assessment Result

**対象者**: {result['participant']}
**実施者**: {result['assessor']}
**実施日時**: {datetime.fromisoformat(result['timestamp']).strftime('%Y年%m月%d日 %H:%M')}

## 分析結果

{result['analysis']}

## 主要な洞察

{chr(10).join([f'- {insight}' for insight in result['insights']])}

---
このレポートは{result['assessor']}により作成されました。
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.logger.info(f"Assessment result saved: {output_path}")
    
    async def create_assessment_questionnaire(self, assessment_type: str) -> List[Dict[str, str]]:
        """Create an assessment questionnaire."""
        
        questionnaire_prompt = f"""
{assessment_type}タイプの性格診断のための質問票を作成してください。

【要件】
- 10-15問程度の質問
- 回答しやすい選択肢形式
- 日本語で自然な表現
- 診断に有効な質問内容

以下の形式で質問を作成してください：

質問1: [質問内容]
A) [選択肢1]
B) [選択肢2] 
C) [選択肢3]
D) [選択肢4]

{self.config.personality.name}として、有効で使いやすい質問票を作成してください。
"""
        
        questionnaire_text = await self.llm.generate_response(questionnaire_prompt)
        
        # Parse questionnaire (simplified implementation)
        questions = []
        current_question = None
        current_options = []
        
        for line in questionnaire_text.split('\n'):
            line = line.strip()
            if line.startswith('質問') and ':' in line:
                if current_question:
                    questions.append({
                        "question": current_question,
                        "options": current_options.copy()
                    })
                current_question = line.split(':', 1)[1].strip()
                current_options = []
            elif line and line[0] in 'ABCD' and ')' in line:
                option = line.split(')', 1)[1].strip()
                current_options.append(option)
        
        if current_question:
            questions.append({
                "question": current_question,
                "options": current_options
            })
        
        return questions