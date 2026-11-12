---
name: slack-emoji
description: 슬랙 커스텀 이모지(128x128 PNG 또는 움직이는 GIF, 128KB 이하)를 텍스트로 만든다. "슬랙 이모지 만들어줘", "이모지 GIF", "반응 이모지" 요청에 사용.
---

# 슬랙 이모지 만들기

1. 사용자에게 받을 것: 문구(짧게, 2~4자 권장, 줄바꿈은 `\n`), 움직임 여부, 색상.
2. 실행:
   `python3 .claude/skills/slack-emoji/scripts/make_emoji.py "문구" 출력파일 --anim 종류 --fg 글자색 --bg 배경색`
   - anim: `none`(PNG) / `shake`(흔들) / `bounce`(통통) / `blink`(깜빡) / `rainbow`(무지개) / `spin`(회전)
   - `--bg none` 이면 투명 배경
3. 결과 파일 크기가 128KB 넘으면 문구 줄이거나 anim 단순화 후 재생성.
4. 결과물을 이미지로 확인하고 사용자에게 파일 전달. 슬랙 업로드: 이모지 추가 > 이미지 업로드 > 이름 지정.
