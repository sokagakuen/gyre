"""Consultation and proposal functionality."""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from ...core.config import AgentConfig
from ...core.llm_interface import LLMInterface


class ConsultationModule:
    """Provide consultations and create proposals."""
    
    def __init__(self, config: AgentConfig, llm: LLMInterface):
        """Initialize the consultation module."""
        self.config = config
        self.llm = llm
        self.logger = logging.getLogger(__name__)
        
        # Consultation types and their approaches
        self.consultation_types = {
            "strategy": "戦略コンサルティング",
            "management": "マネジメント相談",
            "career": "キャリア相談",
            "team": "チーム課題解決",
            "process": "プロセス改善",
            "decision": "意思決定支援",
            "conflict": "対立解決",
            "innovation": "イノベーション支援"
        }
    
    async def provide_consultation(
        self, 
        consultation_type: str, 
        details: Dict[str, Any]
    ) -> str:
        """
        Provide consultation and advice.
        
        Args:
            consultation_type: Type of consultation
            details: Consultation details and context
            
        Returns:
            Consultation response and recommendations
        """
        consultation_name = self.consultation_types.get(consultation_type, consultation_type)
        
        consultation_prompt = f"""
{consultation_name}の相談を受けました。以下の詳細について、専門的な助言をお願いします。

【相談の種類】
{consultation_name}

【相談内容・詳細】
{self._format_consultation_details(details)}

【回答の構成】
1. 現状分析
2. 課題の特定
3. 複数の解決選択肢
4. 推奨アクション
5. 実行計画
6. リスクと注意点
7. 成功のためのポイント

{self.config.personality.name}として、実践的で実行可能なアドバイスを提供してください。
過去の経験と専門知識を活かし、相談者の立場に立った建設的な提案を心がけてください。
"""
        
        consultation_response = await self.llm.generate_response(consultation_prompt)
        
        # Save consultation record
        await self._save_consultation_record(consultation_type, details, consultation_response)
        
        self.logger.info(f"Consultation provided: {consultation_type}")
        return consultation_response
    
    async def make_proposal(
        self, 
        proposal_topic: str, 
        requirements: Dict[str, Any]
    ) -> str:
        """
        Create a comprehensive proposal.
        
        Args:
            proposal_topic: Main topic/title of the proposal
            requirements: Proposal requirements and specifications
            
        Returns:
            Formatted proposal document
        """
        
        proposal_prompt = f"""
以下の内容について、包括的な提案書を作成してください。

【提案テーマ】
{proposal_topic}

【要件・背景情報】
{self._format_proposal_requirements(requirements)}

【提案書の構成】
1. エグゼクティブサマリー
2. 背景と現状分析
3. 提案の概要
4. 詳細な実施計画
5. 必要リソースと予算
6. 期待される効果・ROI
7. リスク分析と対策
8. 実施スケジュール
9. 成功指標とKPI
10. 次のステップ

{self.config.personality.name}として、説得力があり実行可能な提案書を作成してください。
根拠とデータに基づいた論理的な構成で、意思決定者が判断しやすい内容にしてください。
"""
        
        proposal_content = await self.llm.generate_response(proposal_prompt)
        
        # Save proposal document
        await self._save_proposal_document(proposal_topic, requirements, proposal_content)
        
        self.logger.info(f"Proposal created: {proposal_topic}")
        return proposal_content
    
    async def analyze_business_case(
        self, 
        case_description: str, 
        analysis_focus: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a business case and provide structured insights.
        
        Args:
            case_description: Description of the business case
            analysis_focus: Specific areas to focus on
            
        Returns:
            Structured business case analysis
        """
        focus_areas = analysis_focus or [
            "市場機会",
            "競合分析", 
            "リスク評価",
            "財務インパクト",
            "実現可能性"
        ]
        
        analysis_prompt = f"""
以下のビジネスケースについて、包括的な分析を行ってください。

【ビジネスケース】
{case_description}

【分析観点】
{chr(10).join([f'- {focus}' for focus in focus_areas])}

以下の構造で分析結果を提供してください：

【状況分析】
現在の状況と背景の整理

【機会と課題】
- 機会: 
- 課題: 

【各観点での分析】
{chr(10).join([f'【{focus}】' for focus in focus_areas])}

【総合的な判断】
- 推奨度: （高/中/低）
- 主な根拠:
- 条件付き推奨事項:

【アクションプラン】
1. 短期アクション（1-3ヶ月）
2. 中期アクション（3-12ヶ月）
3. 長期アクション（1年以上）

{self.config.personality.name}として、客観的で戦略的な分析を提供してください。
"""
        
        analysis_response = await self.llm.generate_response(analysis_prompt)
        
        # Parse structured response
        structured_analysis = await self.llm.generate_structured_response(
            f"以下の分析を構造化してください:\n{analysis_response}",
            {
                "状況分析": "現在の状況の要約",
                "主要な機会": "特定された機会",
                "主要な課題": "特定された課題", 
                "推奨度": "推奨レベル",
                "根拠": "推奨の根拠",
                "次のステップ": "推奨アクション"
            }
        )
        
        result = {
            "case_description": case_description,
            "analysis_focus": focus_areas,
            "full_analysis": analysis_response,
            "structured_analysis": structured_analysis,
            "analyst": self.config.personality.name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save analysis
        await self._save_business_analysis(result)
        
        self.logger.info("Business case analysis completed")
        return result
    
    async def provide_decision_support(
        self, 
        decision_context: str, 
        options: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Provide decision support analysis.
        
        Args:
            decision_context: Context and background of the decision
            options: List of available options with details
            
        Returns:
            Decision support analysis and recommendations
        """
        
        options_text = ""
        for i, option in enumerate(options, 1):
            options_text += f"\n選択肢{i}: {option.get('name', f'Option {i}')}\n"
            options_text += f"内容: {option.get('description', '')}\n"
            options_text += f"メリット: {option.get('benefits', '')}\n"
            options_text += f"デメリット: {option.get('risks', '')}\n"
            options_text += f"コスト: {option.get('cost', '')}\n"
        
        decision_prompt = f"""
以下の意思決定について、包括的な分析と推奨を行ってください。

【意思決定の背景】
{decision_context}

【検討する選択肢】
{options_text}

【分析フレームワーク】
1. 各選択肢の詳細評価
2. 比較分析マトリックス
3. リスク・ベネフィット分析
4. 実現可能性評価
5. 戦略的適合性
6. 総合的な推奨

以下の観点で各選択肢を評価してください：
- 実現可能性（1-5点）
- 期待される効果（1-5点）
- リスクレベル（1-5点）
- 必要リソース（1-5点）
- 戦略的重要性（1-5点）

{self.config.personality.name}として、意思決定者が自信を持って判断できる分析を提供してください。
"""
        
        decision_analysis = await self.llm.generate_response(decision_prompt)
        
        result = {
            "decision_context": decision_context,
            "options": options,
            "analysis": decision_analysis,
            "recommendation_summary": await self._extract_recommendation(decision_analysis),
            "decision_supporter": self.config.personality.name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save decision support
        await self._save_decision_support(result)
        
        self.logger.info("Decision support analysis completed")
        return result
    
    def _format_consultation_details(self, details: Dict[str, Any]) -> str:
        """Format consultation details for prompt."""
        if not details:
            return "詳細な情報は提供されていません。"
        
        formatted = []
        for key, value in details.items():
            if isinstance(value, list):
                formatted.append(f"{key}: {', '.join(map(str, value))}")
            elif isinstance(value, dict):
                formatted.append(f"{key}: {', '.join([f'{k}: {v}' for k, v in value.items()])}")
            else:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)
    
    def _format_proposal_requirements(self, requirements: Dict[str, Any]) -> str:
        """Format proposal requirements for prompt."""
        return self._format_consultation_details(requirements)
    
    async def _extract_recommendation(self, analysis: str) -> str:
        """Extract key recommendation from analysis."""
        extract_prompt = f"""
以下の分析結果から、最も重要な推奨事項を1-2文で要約してください：

{analysis}

{self.config.personality.name}として、明確で行動しやすい推奨を提供してください。
"""
        
        return await self.llm.generate_response(extract_prompt)
    
    async def _save_consultation_record(
        self, 
        consultation_type: str, 
        details: Dict[str, Any], 
        response: str
    ) -> None:
        """Save consultation record."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"consultation_{consultation_type}_{timestamp}.md"
        output_path = self.config.output_dir / "consultations" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"""# Consultation Record

**種類**: {self.consultation_types.get(consultation_type, consultation_type)}
**実施者**: {self.config.personality.name}
**実施日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

## 相談内容

{self._format_consultation_details(details)}

## 回答・アドバイス

{response}

---
このコンサルテーションは{self.config.personality.name}により実施されました。
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.logger.info(f"Consultation record saved: {output_path}")
    
    async def _save_proposal_document(
        self, 
        topic: str, 
        requirements: Dict[str, Any], 
        content: str
    ) -> None:
        """Save proposal document."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(" ", "_").replace("/", "_")
        filename = f"proposal_{safe_topic}_{timestamp}.md"
        output_path = self.config.output_dir / "proposals" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        document = f"""# {topic}

**提案者**: {self.config.personality.name}
**作成日**: {datetime.now().strftime('%Y年%m月%d日')}

{content}

---
この提案書は{self.config.personality.name}により作成されました。
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(document)
        
        self.logger.info(f"Proposal document saved: {output_path}")
    
    async def _save_business_analysis(self, analysis: Dict[str, Any]) -> None:
        """Save business case analysis."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"business_analysis_{timestamp}.md"
        output_path = self.config.output_dir / "analyses" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"""# Business Case Analysis

**分析者**: {analysis['analyst']}
**分析日時**: {datetime.fromisoformat(analysis['timestamp']).strftime('%Y年%m月%d日 %H:%M')}

## ビジネスケース

{analysis['case_description']}

## 分析結果

{analysis['full_analysis']}

## 構造化された分析

{chr(10).join([f"**{key}**: {value}" for key, value in analysis['structured_analysis'].items()])}

---
この分析は{analysis['analyst']}により実施されました。
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.logger.info(f"Business analysis saved: {output_path}")
    
    async def _save_decision_support(self, decision_data: Dict[str, Any]) -> None:
        """Save decision support analysis."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"decision_support_{timestamp}.md"
        output_path = self.config.output_dir / "decisions" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        content = f"""# Decision Support Analysis

**意思決定支援者**: {decision_data['decision_supporter']}
**分析日時**: {datetime.fromisoformat(decision_data['timestamp']).strftime('%Y年%m月%d日 %H:%M')}

## 意思決定の背景

{decision_data['decision_context']}

## 検討された選択肢

{chr(10).join([f"- {option.get('name', 'Option')}: {option.get('description', '')}" for option in decision_data['options']])}

## 分析結果

{decision_data['analysis']}

## 推奨サマリー

{decision_data['recommendation_summary']}

---
この意思決定支援は{decision_data['decision_supporter']}により実施されました。
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.logger.info(f"Decision support saved: {output_path}")