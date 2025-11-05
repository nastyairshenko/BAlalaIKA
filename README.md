1) Python 3.11, локально:
python -m venv .venv && .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env  # заполните TG_BOT_TOKEN и LLM_API_KEY
python -m src.bot.tg_bot

2) Команды:
 /start /help /topic <тема> /roleplay /cancel

3) Архитектура:
- VAD (Valence по тексту) -> Moral Schemas -> Action Preset -> LLM (DeepSeek).
- Схемы: mentorship, comradeship, social_empathy, professional_help + 6 дидактических (warmup, gentle correction, roleplay, celebrate, flow switch, micro-goal).
