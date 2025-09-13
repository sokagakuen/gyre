# {{ meeting_title }} - 議事録

**日時**: {{ date }}  
**場所**: {{ location | default("オンライン") }}  
**ファシリテーター**: {{ facilitator }}  
**記録者**: {{ recorder | default(facilitator) }}

## 参加者

{% if participants %}
{% for participant in participants %}
- {{ participant }}
{% endfor %}
{% else %}
- 参加者リストを記載
{% endif %}

## アジェンダ

{% if agenda %}
{% for item in agenda %}
{{ loop.index }}. {{ item }}
{% endfor %}
{% else %}
1. 開会・前回議事録の確認
2. 主要議題の議論
3. 決定事項の確認
4. 次回予定の確認
{% endif %}

## 議論内容

{% if discussions %}
{% for discussion in discussions %}
### {{ discussion.topic }}

**議論のポイント:**
{{ discussion.points }}

**主な意見:**
{{ discussion.opinions }}

{% endfor %}
{% else %}
### [議題1]
- 議論のポイント
- 出された意見
- 検討事項

### [議題2]
- 議論のポイント
- 出された意見
- 検討事項
{% endif %}

## 決定事項

{% if decisions %}
{% for decision in decisions %}
{{ loop.index }}. {{ decision }}
{% endfor %}
{% else %}
1. 決定事項を記載
2. 合意された内容
3. 承認された提案
{% endif %}

## アクションアイテム

| 項目 | 担当者 | 期限 | ステータス |
|------|--------|------|-----------|
{% if action_items %}
{% for item in action_items %}
| {{ item.task }} | {{ item.assignee }} | {{ item.deadline }} | {{ item.status | default("未着手") }} |
{% endfor %}
{% else %}
| アクション項目 | 担当者名 | 期限 | 未着手 |
| フォローアップ項目 | 担当者名 | 期限 | 未着手 |
{% endif %}

## 次回予定

**日時**: {{ next_meeting_date | default("未定") }}  
**議題**: {{ next_meeting_agenda | default("今回のフォローアップおよび新規議題") }}

## 補足事項

{% if notes %}
{{ notes }}
{% else %}
- 重要な補足事項があれば記載
- 参考資料や関連情報
- その他の連絡事項
{% endif %}

---
**記録者**: {{ recorder | default(facilitator) }}  
**承認者**: {{ approver | default("参加者全員") }}  
**作成日**: {{ date }}