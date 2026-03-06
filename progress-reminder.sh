#!/bin/bash
# 🐍 贪吃蛇开发进度提醒脚本
# 每 2 分钟发送一次提醒到 Telegram 群

TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
CHAT_ID="-5231910665"

# 如果设置了 Bot Token，直接调用 Telegram API
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${CHAT_ID}" \
        -d "text=⏰ 贪吃蛇开发进度检查点

🐍 @boboclaw1016_bot 该汇报进度了！

请汇报：
✅ 过去 2 分钟完成了什么
📦 交付物（commit/文件）
⚠️ 遇到的问题
🎯 下一个 2 分钟目标

记住：没交付就承认没进展！" \
        -d "parse_mode=Markdown" > /dev/null
else
    # 没有 Bot Token 时，写入日志文件
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⏰ 进度检查点 - 请 @boboclaw1016_bot 汇报" >> /Users/hujinbo/.openclaw/workspace/snake-game/progress-check.log
fi
