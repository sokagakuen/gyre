"""Document generation functionality."""

import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
import yaml
import logging

from jinja2 import Environment, FileSystemLoader, Template

from ...core.config import AgentConfig
from ...core.llm_interface import LLMInterface


class DocumentGenerator:
    """Generate documents using templates and AI assistance."""
    
    def __init__(self, config: AgentConfig, llm: LLMInterface):
        """Initialize the document generator."""
        self.config = config
        self.llm = llm
        self.logger = logging.getLogger(__name__)
        
        # Setup Jinja2 environment
        if self.config.document_templates.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(self.config.document_templates)),
                enable_async=True
            )
        else:
            self.jinja_env = None
    
    async def generate_document(
        self, 
        doc_type: str, 
        topic: str, 
        requirements: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a document based on type, topic, and requirements.
        
        Args:
            doc_type: Type of document (e.g., 'proposal', 'report', 'memo')
            topic: Main topic or title of the document
            requirements: Additional requirements and specifications
            
        Returns:
            Generated document content
        """
        requirements = requirements or {}
        
        # Try to use template first
        if self.jinja_env:
            template_path = f"{doc_type}.md"
            try:
                template = self.jinja_env.get_template(template_path)
                base_content = await self._generate_with_template(template, topic, requirements)
            except Exception as e:
                self.logger.warning(f"Template not found or error: {e}, falling back to AI generation")
                base_content = await self._generate_with_ai(doc_type, topic, requirements)
        else:
            base_content = await self._generate_with_ai(doc_type, topic, requirements)
        
        # Save the generated document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{doc_type}_{topic.replace(' ', '_')}_{timestamp}.md"
        output_path = self.config.output_dir / "documents" / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(base_content)
        
        self.logger.info(f"Document generated: {output_path}")
        return base_content
    
    async def _generate_with_template(
        self, 
        template: Template, 
        topic: str, 
        requirements: Dict[str, Any]
    ) -> str:
        """Generate document using Jinja2 template."""
        # Generate content for template variables using AI
        template_vars = {
            "topic": topic,
            "date": datetime.now().strftime("%Y年%m月%d日"),
            "author": self.config.personality.name,
            **requirements
        }
        
        # Generate dynamic content if needed
        if "content_sections" in requirements:
            for section in requirements["content_sections"]:
                section_prompt = f"""
{topic}について、以下のセクションの内容を作成してください：

セクション名: {section}
要件: {requirements.get('section_requirements', {}).get(section, '')}

{self.config.personality.name}として、専門的で実用的な内容を提供してください。
"""
                section_content = await self.llm.generate_response(section_prompt)
                template_vars[f"section_{section.lower().replace(' ', '_')}"] = section_content
        
        return await template.render_async(**template_vars)
    
    async def _generate_with_ai(
        self, 
        doc_type: str, 
        topic: str, 
        requirements: Dict[str, Any]
    ) -> str:
        """Generate document using AI without template."""
        
        doc_type_prompts = {
            "proposal": "提案書",
            "report": "報告書", 
            "memo": "メモ・連絡事項",
            "meeting_minutes": "議事録",
            "strategy": "戦略文書",
            "plan": "計画書",
            "analysis": "分析レポート",
            "presentation": "プレゼンテーション資料"
        }
        
        japanese_doc_type = doc_type_prompts.get(doc_type, doc_type)
        
        prompt = f"""
{japanese_doc_type}を作成してください。

【文書情報】
- 種類: {japanese_doc_type}
- テーマ: {topic}
- 作成者: {self.config.personality.name}
- 作成日: {datetime.now().strftime("%Y年%m月%d日")}

【要件】
{self._format_requirements(requirements)}

【作成方針】
- 読み手にとって理解しやすい構成
- 実用的で行動に移しやすい内容
- 根拠と論理的な説明
- 適切な日本語表現

以下の形式で{japanese_doc_type}を作成してください：

# {topic}

## 概要

## 背景・目的

## 内容詳細

## 結論・提案

## 次のステップ

---
作成者: {self.config.personality.name}
作成日: {datetime.now().strftime("%Y年%m月%d日")}
"""
        
        return await self.llm.generate_response(prompt)
    
    def _format_requirements(self, requirements: Dict[str, Any]) -> str:
        """Format requirements for the prompt."""
        if not requirements:
            return "特別な要件はありません。"
        
        formatted = []
        for key, value in requirements.items():
            if isinstance(value, list):
                formatted.append(f"- {key}: {', '.join(map(str, value))}")
            else:
                formatted.append(f"- {key}: {value}")
        
        return "\n".join(formatted)
    
    async def create_template(self, doc_type: str, template_content: str) -> None:
        """Create a new document template."""
        template_path = self.config.document_templates / f"{doc_type}.md"
        template_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)
        
        self.logger.info(f"Template created: {template_path}")
    
    async def list_available_templates(self) -> List[str]:
        """List available document templates."""
        if not self.config.document_templates.exists():
            return []
        
        templates = []
        for template_file in self.config.document_templates.glob("*.md"):
            templates.append(template_file.stem)
        
        return templates