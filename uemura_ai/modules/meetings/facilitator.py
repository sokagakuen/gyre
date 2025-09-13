"""Meeting facilitation functionality."""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging

from ...core.config import AgentConfig
from ...core.llm_interface import LLMInterface


class MeetingFacilitator:
    """Facilitate meetings and build consensus."""
    
    def __init__(self, config: AgentConfig, llm: LLMInterface):
        """Initialize the meeting facilitator."""
        self.config = config
        self.llm = llm
        self.logger = logging.getLogger(__name__)
    
    async def facilitate_meeting(
        self, 
        meeting_type: str, 
        agenda: List[str], 
        participants: List[str],
        duration_minutes: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Facilitate a meeting session.
        
        Args:
            meeting_type: Type of meeting (e.g., 'kickoff', 'review', 'planning')
            agenda: List of agenda items
            participants: List of participant names
            duration_minutes: Meeting duration in minutes
            
        Returns:
            Meeting facilitation plan and guidance
        """
        duration = duration_minutes or self.config.default_meeting_duration
        
        facilitation_prompt = f"""
会議ファシリテーションをお願いします。

【会議情報】
- 種類: {meeting_type}
- 参加者: {', '.join(participants)} ({len(participants)}名)
- 予定時間: {duration}分
- ファシリテーター: {self.config.personality.name}

【アジェンダ】
{chr(10).join([f'{i+1}. {item}' for i, item in enumerate(agenda)])}

以下の項目について、効果的な会議進行プランを作成してください：

1. 開始時の挨拶と導入
2. 各アジェンダ項目の進行方法と時間配分
3. 参加者の発言を促す質問例
4. 合意形成のための技法
5. 次のアクションの決定方法
6. 会議終了時のまとめ

{self.config.personality.name}として、建設的で効率的な会議になるよう進行してください。
"""
        
        facilitation_plan = await self.llm.generate_response(facilitation_prompt)
        
        # Generate time allocation
        time_per_agenda = (duration - 10) // len(agenda)  # 10 minutes for opening/closing
        agenda_schedule = []
        current_time = datetime.now()
        
        for i, item in enumerate(agenda):
            start_time = current_time + timedelta(minutes=5 + (i * time_per_agenda))
            end_time = start_time + timedelta(minutes=time_per_agenda)
            agenda_schedule.append({
                "item": item,
                "start_time": start_time.strftime("%H:%M"),
                "end_time": end_time.strftime("%H:%M"),
                "duration_minutes": time_per_agenda
            })
        
        result = {
            "meeting_type": meeting_type,
            "participants": participants,
            "agenda": agenda,
            "duration_minutes": duration,
            "facilitation_plan": facilitation_plan,
            "schedule": agenda_schedule,
            "facilitator": self.config.personality.name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save meeting plan
        await self._save_meeting_plan(result)
        
        self.logger.info(f"Meeting facilitation plan created: {meeting_type}")
        return result
    
    async def conduct_one_on_one(
        self, 
        participant_name: str, 
        topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Conduct a 1-on-1 session.
        
        Args:
            participant_name: Name of the participant
            topics: Optional list of topics to discuss
            
        Returns:
            1-on-1 session plan and guidance
        """
        topics = topics or [
            "最近の業務状況",
            "成果と課題", 
            "今後の目標",
            "必要なサポート",
            "その他の相談事項"
        ]
        
        one_on_one_prompt = f"""
{participant_name}さんとの1on1ミーティングを実施します。

【1on1情報】
- 参加者: {participant_name}さん
- ファシリテーター: {self.config.personality.name}
- 予定時間: 30分

【話し合いたいトピック】
{chr(10).join([f'- {topic}' for topic in topics])}

以下について、効果的な1on1の進行プランを作成してください：

1. 場作りとアイスブレイク
2. 各トピックでの質問例と進め方
3. 相手の話を引き出すコミュニケーション技法
4. フィードバックとアドバイスの方法
5. 次回までのアクションプラン設定
6. 1on1終了時のまとめ

{self.config.personality.name}として、{participant_name}さんが安心して話せる雰囲気を作り、
有意義な時間になるよう進行してください。
"""
        
        session_plan = await self.llm.generate_response(one_on_one_prompt)
        
        result = {
            "session_type": "1on1",
            "participant": participant_name,
            "topics": topics,
            "session_plan": session_plan,
            "facilitator": self.config.personality.name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save 1-on-1 plan
        await self._save_meeting_plan(result)
        
        self.logger.info(f"1-on-1 session plan created for: {participant_name}")
        return result
    
    async def generate_meeting_minutes(
        self, 
        meeting_info: Dict[str, Any], 
        discussion_points: List[str],
        decisions: List[str],
        action_items: List[Dict[str, str]]
    ) -> str:
        """
        Generate meeting minutes.
        
        Args:
            meeting_info: Basic meeting information
            discussion_points: Key discussion points
            decisions: Decisions made
            action_items: Action items with assignees and deadlines
            
        Returns:
            Formatted meeting minutes
        """
        minutes_prompt = f"""
以下の会議の議事録を作成してください。

【会議情報】
- 会議名: {meeting_info.get('meeting_type', '会議')}
- 日時: {meeting_info.get('date', datetime.now().strftime('%Y年%m月%d日'))}
- 参加者: {', '.join(meeting_info.get('participants', []))}
- ファシリテーター: {self.config.personality.name}

【主な議論内容】
{chr(10).join([f'- {point}' for point in discussion_points])}

【決定事項】
{chr(10).join([f'- {decision}' for decision in decisions])}

【アクションアイテム】
{chr(10).join([f'- {item["task"]} (担当: {item["assignee"]}, 期限: {item["deadline"]})' for item in action_items])}

正式な議事録の形式で、分かりやすく整理してください。
"""
        
        minutes = await self.llm.generate_response(minutes_prompt)
        
        # Save meeting minutes
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"meeting_minutes_{timestamp}.md"
        output_path = self.config.output_dir / "meetings" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(minutes)
        
        self.logger.info(f"Meeting minutes saved: {output_path}")
        return minutes
    
    async def _save_meeting_plan(self, plan_data: Dict[str, Any]) -> None:
        """Save meeting plan to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_type = plan_data.get('session_type', plan_data.get('meeting_type', 'meeting'))
        filename = f"{session_type}_plan_{timestamp}.md"
        output_path = self.config.output_dir / "meetings" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Format the plan data as markdown
        content = f"""# {session_type.title()} Plan

**日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
**ファシリテーター**: {plan_data['facilitator']}

"""
        
        if 'participants' in plan_data:
            content += f"**参加者**: {', '.join(plan_data['participants'])}\n\n"
        elif 'participant' in plan_data:
            content += f"**参加者**: {plan_data['participant']}\n\n"
        
        if 'agenda' in plan_data:
            content += "## アジェンダ\n"
            for i, item in enumerate(plan_data['agenda'], 1):
                content += f"{i}. {item}\n"
            content += "\n"
        
        if 'topics' in plan_data:
            content += "## トピック\n"
            for topic in plan_data['topics']:
                content += f"- {topic}\n"
            content += "\n"
        
        if 'schedule' in plan_data:
            content += "## タイムスケジュール\n"
            for item in plan_data['schedule']:
                content += f"- {item['start_time']}-{item['end_time']}: {item['item']}\n"
            content += "\n"
        
        content += "## 進行プラン\n\n"
        content += plan_data.get('facilitation_plan', plan_data.get('session_plan', ''))
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        self.logger.info(f"Meeting plan saved: {output_path}")