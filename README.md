# 上村仁 AI Agent (Uemura Jin AI Agent)

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-alpha-orange.svg)

上村仁の代わりを担当するAIエージェントシステム。思考、資料作成、会議進行、合意形成、1on1、性格診断、相談・提案など、包括的な業務支援を提供します。

## 🤖 概要

このAIエージェントは以下の機能を提供します：

- **思考支援**: 上村仁として複雑な問題について深く考え、洞察を提供
- **文書作成**: 提案書、報告書、議事録など各種文書の自動生成
- **会議ファシリテーション**: 効果的な会議進行と合意形成の支援
- **1on1セッション**: 個人面談の計画と実施支援
- **性格診断**: MBTI、Big Five、DISC、強み診断などの実施
- **コンサルテーション**: 戦略、マネジメント、キャリアなど各種相談対応
- **提案作成**: ビジネス提案書の作成と意思決定支援

## 🚀 クイックスタート

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/sokagakuen/gyre.git
cd gyre

# 依存関係をインストール
pip install -r requirements.txt

# 初期セットアップ
python -m uemura_ai.cli setup
```

### 環境設定

1. `.env`ファイルを作成（`.env.example`を参考）:
```bash
cp .env.example .env
```

2. AIモデルのAPIキーを設定:
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 使用方法

#### インタラクティブセッション
```bash
python -m uemura_ai.cli interactive
```

#### コマンドライン使用例

**思考・相談**:
```bash
python -m uemura_ai.cli think "新しいプロジェクトの戦略について考えてください"
```

**文書作成**:
```bash
python -m uemura_ai.cli document proposal "AIプロジェクト提案" --req '{"budget": "500万円", "duration": "6ヶ月"}'
```

**会議ファシリテーション**:
```bash
python -m uemura_ai.cli meeting kickoff "プロジェクト開始,役割分担,スケジュール確認" "田中,佐藤,鈴木"
```

**1on1セッション**:
```bash
python -m uemura_ai.cli one-on-one "田中さん" --topics "最近の業務,今後の目標,必要なサポート"
```

**性格診断**:
```bash
python -m uemura_ai.cli assessment mbti --participant "田中さん"
```

**コンサルテーション**:
```bash
python -m uemura_ai.cli consult strategy "新規事業の参入戦略について相談したい"
```

## 📚 機能詳細

### 1. 思考支援 (Think)
上村仁の視点で複雑な問題を分析し、洞察を提供します。

**特徴**:
- 多角的な視点での分析
- 実践的で行動可能な提案
- 豊富な経験に基づいた判断

### 2. 文書生成 (Document Generation)
各種ビジネス文書を自動生成します。

**対応文書タイプ**:
- `proposal`: 提案書
- `report`: 報告書  
- `memo`: メモ・連絡事項
- `meeting_minutes`: 議事録
- `strategy`: 戦略文書
- `plan`: 計画書
- `analysis`: 分析レポート

### 3. 会議ファシリテーション (Meeting Facilitation)
効果的な会議進行をサポートします。

**提供機能**:
- 会議進行プランの作成
- タイムスケジュールの管理
- 参加者の発言促進
- 合意形成の支援
- 議事録の自動生成

### 4. 1on1セッション (One-on-One)
個人面談の計画と実施を支援します。

**提供機能**:
- セッションプランの作成
- 効果的な質問例の提供
- 話しやすい雰囲気作り
- フォローアップ計画

### 5. 性格診断 (Personality Assessment)
科学的根拠に基づいた性格診断を実施します。

**対応診断**:
- `mbti`: MBTI 16タイプ性格診断
- `big5`: Big Five 性格特性
- `disc`: DISC 行動特性
- `strengths`: 強み診断

### 6. コンサルテーション (Consultation)
専門的な助言とサポートを提供します。

**相談分野**:
- `strategy`: 戦略コンサルティング
- `management`: マネジメント相談
- `career`: キャリア相談
- `team`: チーム課題解決
- `process`: プロセス改善
- `decision`: 意思決定支援
- `conflict`: 対立解決
- `innovation`: イノベーション支援

## 🔧 カスタマイズ

### 性格設定
`config/personality.yaml`でエージェントの性格や行動特性をカスタマイズできます。

```yaml
name: "上村仁"
communication_style: "polite_formal"
expertise_areas:
  - "management"
  - "strategy"
  - "team_leadership"
personality_traits:
  openness: 0.8
  conscientiousness: 0.9
  extraversion: 0.7
  agreeableness: 0.8
  neuroticism: 0.2
```

### テンプレート
`templates/`ディレクトリでドキュメントテンプレートをカスタマイズできます。

## 📁 プロジェクト構造

```
gyre/
├── uemura_ai/                 # メインパッケージ
│   ├── core/                  # コア機能
│   │   ├── agent.py          # メインエージェントクラス
│   │   ├── config.py         # 設定管理
│   │   └── llm_interface.py  # AIモデルインターフェース
│   ├── modules/              # 機能モジュール
│   │   ├── documents/        # 文書生成
│   │   ├── meetings/         # 会議ファシリテーション
│   │   ├── assessments/      # 性格診断
│   │   └── consultation/     # コンサルテーション
│   └── cli.py               # コマンドラインインターフェース
├── templates/               # 文書テンプレート
├── config/                 # 設定ファイル
├── output/                # 生成ファイル出力先
└── logs/                  # ログファイル
```

## 🔄 ワークフロー例

### 新規プロジェクト立ち上げ

1. **戦略相談**:
```bash
python -m uemura_ai.cli consult strategy "新規AIプロジェクトの立ち上げ戦略"
```

2. **提案書作成**:
```bash
python -m uemura_ai.cli proposal "AIプロジェクト提案書"
```

3. **キックオフ会議**:
```bash
python -m uemura_ai.cli meeting kickoff "プロジェクト概要,役割分担,スケジュール" "チームメンバー"
```

4. **チーム診断**:
```bash
python -m uemura_ai.cli assessment disc --participant "チームメンバー"
```

5. **定期1on1**:
```bash
python -m uemura_ai.cli one-on-one "メンバー名"
```

## 🧪 開発・テスト

### 開発環境のセットアップ
```bash
pip install -e ".[dev]"
```

### テスト実行
```bash
pytest
```

### コード品質チェック
```bash
black uemura_ai/
flake8 uemura_ai/
mypy uemura_ai/
```

## 📝 API使用例

### Python API

```python
from uemura_ai import UemuraJinAgent, AgentConfig

# エージェント初期化
config = AgentConfig()
agent = UemuraJinAgent(config)

# 思考・相談
response = await agent.think("プロジェクトの課題について")

# 文書作成
document = await agent.create_document("proposal", "新規事業提案")

# 会議ファシリテーション
meeting_plan = await agent.facilitate_meeting(
    "planning", 
    ["現状分析", "課題整理", "解決策検討"], 
    ["田中", "佐藤", "鈴木"]
)

# 性格診断
assessment = await agent.assess_personality(
    "mbti", 
    {"responses": user_responses}
)
```

## 🤝 貢献

プロジェクトへの貢献を歓迎します！

1. フォークしてください
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを開いてください

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。

## 📞 サポート

- 問題や質問: [GitHub Issues](https://github.com/sokagakuen/gyre/issues)
- 機能要望: [GitHub Discussions](https://github.com/sokagakuen/gyre/discussions)

## 🔄 ロードマップ

- [ ] Web インターフェースの追加
- [ ] 多言語対応の拡張
- [ ] 音声インターフェースの実装
- [ ] チーム管理機能の追加
- [ ] 統合ダッシュボードの開発
- [ ] モバイルアプリの開発

---

**上村仁AIエージェント** - あなたの思考パートナー 🤖