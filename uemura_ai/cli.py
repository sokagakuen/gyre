"""Command Line Interface for the Uemura Jin AI Agent."""

import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .core.agent import UemuraJinAgent
from .core.config import AgentConfig

app = typer.Typer(help="上村仁 AI Agent - Command Line Interface")
console = Console()


@app.command()
def interactive():
    """Start an interactive session with the Uemura Jin AI Agent."""
    try:
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        console.print(Panel.fit(
            f"[bold blue]上村仁 AI エージェント[/bold blue]\n"
            f"対話セッションを開始します",
            title="🤖 AI Agent"
        ))
        
        asyncio.run(agent.interactive_session())
        
    except KeyboardInterrupt:
        console.print("\n[yellow]セッションを終了します。[/yellow]")
    except Exception as e:
        console.print(f"[red]エラーが発生しました: {e}[/red]")


@app.command()
def think(
    query: str = typer.Argument(..., help="思考してもらいたい内容"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="追加のコンテキスト情報")
):
    """Ask the agent to think about a specific topic."""
    async def _think():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        context_dict = {"additional_info": context} if context else None
        response = await agent.think(query, context_dict)
        
        console.print(Panel(
            response,
            title=f"🤔 {config.personality.name}の思考",
            title_align="left"
        ))
    
    asyncio.run(_think())


@app.command()
def document(
    doc_type: str = typer.Argument(..., help="文書の種類 (proposal, report, memo, etc.)"),
    topic: str = typer.Argument(..., help="文書のトピック"),
    requirements: Optional[str] = typer.Option(None, "--req", "-r", help="追加要件 (JSON形式)")
):
    """Generate a document."""
    async def _generate_document():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        req_dict = {}
        if requirements:
            try:
                import json
                req_dict = json.loads(requirements)
            except json.JSONDecodeError:
                console.print("[yellow]要件のJSON形式が無効です。空の要件で続行します。[/yellow]")
        
        console.print(f"[blue]文書を生成中: {doc_type} - {topic}[/blue]")
        document_content = await agent.create_document(doc_type, topic, req_dict)
        
        console.print(Panel(
            document_content,
            title=f"📄 {doc_type} - {topic}",
            title_align="left"
        ))
    
    asyncio.run(_generate_document())


@app.command()
def meeting(
    meeting_type: str = typer.Argument(..., help="会議の種類"),
    agenda: str = typer.Argument(..., help="アジェンダ項目 (カンマ区切り)"),
    participants: str = typer.Argument(..., help="参加者 (カンマ区切り)"),
    duration: Optional[int] = typer.Option(60, "--duration", "-d", help="会議時間（分）")
):
    """Facilitate a meeting."""
    async def _facilitate_meeting():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        agenda_list = [item.strip() for item in agenda.split(",")]
        participants_list = [person.strip() for person in participants.split(",")]
        
        console.print(f"[blue]会議ファシリテーションプランを作成中...[/blue]")
        meeting_plan = await agent.facilitate_meeting(
            meeting_type, agenda_list, participants_list, duration
        )
        
        # Display meeting plan in a table
        table = Table(title=f"会議プラン: {meeting_type}")
        table.add_column("項目", style="cyan")
        table.add_column("内容", style="white")
        
        table.add_row("会議種類", meeting_plan["meeting_type"])
        table.add_row("参加者", ", ".join(meeting_plan["participants"]))
        table.add_row("予定時間", f"{meeting_plan['duration_minutes']}分")
        table.add_row("ファシリテーター", meeting_plan["facilitator"])
        
        console.print(table)
        
        console.print(Panel(
            meeting_plan["facilitation_plan"],
            title="📋 ファシリテーションプラン",
            title_align="left"
        ))
    
    asyncio.run(_facilitate_meeting())


@app.command()
def one_on_one(
    participant: str = typer.Argument(..., help="参加者名"),
    topics: Optional[str] = typer.Option(None, "--topics", "-t", help="話し合いたいトピック (カンマ区切り)")
):
    """Conduct a 1-on-1 session."""
    async def _conduct_one_on_one():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        topics_list = None
        if topics:
            topics_list = [topic.strip() for topic in topics.split(",")]
        
        console.print(f"[blue]1on1セッションプランを作成中: {participant}[/blue]")
        session_plan = await agent.conduct_one_on_one(participant, topics_list)
        
        console.print(Panel(
            session_plan["session_plan"],
            title=f"👥 1on1 with {participant}",
            title_align="left"
        ))
    
    asyncio.run(_conduct_one_on_one())


@app.command()
def assessment(
    assessment_type: str = typer.Argument(..., help="評価の種類 (mbti, big5, disc, strengths)"),
    participant: Optional[str] = typer.Option(None, "--participant", "-p", help="評価対象者名"),
    responses_file: Optional[str] = typer.Option(None, "--responses", "-r", help="回答データファイル (JSON)")
):
    """Conduct personality assessment."""
    async def _conduct_assessment():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        responses = {}
        if responses_file:
            try:
                import json
                with open(responses_file, 'r', encoding='utf-8') as f:
                    responses = json.load(f)
            except Exception as e:
                console.print(f"[red]回答ファイル読み込みエラー: {e}[/red]")
                return
        else:
            # Interactive response collection
            console.print(f"[blue]{assessment_type}評価のための簡単な情報を収集します[/blue]")
            responses["behavioral_observations"] = typer.prompt("行動・性格の観察結果を入力してください")
            responses["work_style"] = typer.prompt("仕事のスタイルについて入力してください")
            responses["communication_style"] = typer.prompt("コミュニケーションスタイルについて入力してください")
        
        console.print(f"[blue]性格評価を実施中: {assessment_type}[/blue]")
        assessment_result = await agent.assess_personality(assessment_type, responses, participant)
        
        console.print(Panel(
            assessment_result["analysis"],
            title=f"🎯 {assessment_result['framework']} Assessment",
            title_align="left"
        ))
        
        if assessment_result["insights"]:
            console.print("\n[bold]主要な洞察:[/bold]")
            for insight in assessment_result["insights"]:
                console.print(f"• {insight}")
    
    asyncio.run(_conduct_assessment())


@app.command()
def consult(
    consultation_type: str = typer.Argument(..., help="相談の種類 (strategy, management, career, etc.)"),
    description: str = typer.Argument(..., help="相談内容の説明"),
    details_file: Optional[str] = typer.Option(None, "--details", "-d", help="詳細情報ファイル (JSON)")
):
    """Get consultation and advice."""
    async def _provide_consultation():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        details = {"description": description}
        if details_file:
            try:
                import json
                with open(details_file, 'r', encoding='utf-8') as f:
                    file_details = json.load(f)
                details.update(file_details)
            except Exception as e:
                console.print(f"[yellow]詳細ファイル読み込みエラー: {e}[/yellow]")
        
        console.print(f"[blue]コンサルテーションを実施中: {consultation_type}[/blue]")
        consultation_response = await agent.provide_consultation(consultation_type, details)
        
        console.print(Panel(
            consultation_response,
            title=f"💡 {consultation_type.title()} コンサルテーション",
            title_align="left"
        ))
    
    asyncio.run(_provide_consultation())


@app.command()
def proposal(
    topic: str = typer.Argument(..., help="提案のトピック"),
    requirements_file: Optional[str] = typer.Option(None, "--requirements", "-r", help="要件ファイル (JSON)")
):
    """Create a proposal."""
    async def _make_proposal():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        requirements = {}
        if requirements_file:
            try:
                import json
                with open(requirements_file, 'r', encoding='utf-8') as f:
                    requirements = json.load(f)
            except Exception as e:
                console.print(f"[yellow]要件ファイル読み込みエラー: {e}[/yellow]")
        
        console.print(f"[blue]提案書を作成中: {topic}[/blue]")
        proposal_content = await agent.make_proposal(topic, requirements)
        
        console.print(Panel(
            proposal_content,
            title=f"📋 Proposal: {topic}",
            title_align="left"
        ))
    
    asyncio.run(_make_proposal())


@app.command()
def consensus(
    topic: str = typer.Argument(..., help="合意形成が必要なトピック"),
    positions_file: str = typer.Argument(..., help="ステークホルダーの立場を記載したファイル (JSON)")
):
    """Build consensus among stakeholders."""
    async def _build_consensus():
        config = AgentConfig()
        agent = UemuraJinAgent(config)
        
        try:
            import json
            with open(positions_file, 'r', encoding='utf-8') as f:
                stakeholder_positions = json.load(f)
        except Exception as e:
            console.print(f"[red]立場ファイル読み込みエラー: {e}[/red]")
            return
        
        console.print(f"[blue]合意形成支援を実施中: {topic}[/blue]")
        consensus_result = await agent.build_consensus(topic, stakeholder_positions)
        
        console.print(Panel(
            consensus_result["consensus_proposal"],
            title=f"🤝 合意形成: {topic}",
            title_align="left"
        ))
    
    asyncio.run(_build_consensus())


@app.command()
def config_show():
    """Show current configuration."""
    config = AgentConfig()
    
    table = Table(title="Current Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Agent Name", config.personality.name)
    table.add_row("Language", config.personality.language)
    table.add_row("Communication Style", config.personality.communication_style)
    table.add_row("Default Model", config.ai_model.default_model)
    table.add_row("Temperature", str(config.ai_model.temperature))
    table.add_row("Output Directory", str(config.output_dir))
    
    console.print(table)


@app.command()
def setup():
    """Setup the agent configuration."""
    console.print("[bold blue]上村仁 AI Agent Setup[/bold blue]")
    
    # Check if config directory exists
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)
    
    # Create default personality config
    personality_config = {
        "name": "上村仁",
        "language": "ja",
        "communication_style": "polite_formal",
        "expertise_areas": ["management", "strategy", "team_leadership"],
        "decision_making_style": "analytical_collaborative",
        "meeting_style": "facilitative_consensus_building",
        "personality_traits": {
            "openness": 0.8,
            "conscientiousness": 0.9,
            "extraversion": 0.7,
            "agreeableness": 0.8,
            "neuroticism": 0.2
        }
    }
    
    import yaml
    with open(config_dir / "personality.yaml", "w", encoding="utf-8") as f:
        yaml.dump(personality_config, f, default_flow_style=False, allow_unicode=True)
    
    # Ensure directories exist
    config = AgentConfig()
    config.ensure_directories()
    
    console.print("[green]✓ セットアップが完了しました[/green]")
    console.print("設定ファイルとディレクトリが作成されました。")
    console.print("\n次のステップ:")
    console.print("1. .env ファイルを作成してAPI keyを設定")
    console.print("2. uemura-ai interactive でインタラクティブセッションを開始")


def main():
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()