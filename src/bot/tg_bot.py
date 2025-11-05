import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand
from aiogram.filters import Command, CommandStart
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.core.config import Cfg
from src.tutor.virtual_tutor import VirtualTutor
from src.tutor.emotion_fusion import fuse

bot = Bot(Cfg.TG_TOKEN)
dp = Dispatcher()
tutor = VirtualTutor()
analyzer = SentimentIntensityAnalyzer()

# простая «память»
user_topics: dict[int, str] = {}
pending_topic: set[int] = set()

def looks_like_topic(text: str) -> bool:
    """очень простая эвристика: короткая фраза без пунктуации → вероятно тема"""
    t = text.strip()
    return len(t.split()) <= 3 and all(ch.isalnum() or ch.isspace() for ch in t)

@dp.message(CommandStart())
async def cmd_start(m: Message):
    await bot.set_my_commands([
        BotCommand(command="start",    description="Приветствие"),
        BotCommand(command="help",     description="Подсказка"),
        BotCommand(command="topic",    description="Задать тему разговора"),
        BotCommand(command="roleplay", description="Ролевая сцена по теме"),
        BotCommand(command="cancel",   description="Отмена шага"),
    ])
    pending_topic.add(m.from_user.id)
    await m.answer("Привет! На какую тему поговорим? Напиши одним-двумя словами, например: coffee shop / job interview / travel")

@dp.message(Command("help"))
async def cmd_help(m: Message):
    await m.answer("Напиши тему одним словом (напр. *coffee shop*) — или используй /topic <тема>. Потом просто общайся, я буду мягко корректировать и задавать вопросы.")

@dp.message(Command("topic"))
async def cmd_topic(m: Message):
    uid = m.from_user.id
    args = m.text.split(maxsplit=1)
    if len(args) == 1 or not args[1].strip():
        pending_topic.add(uid)
        await m.answer("Окей! Напиши следующим сообщением тему (например: coffee shop).")
        return
    topic = args[1].strip()
    user_topics[uid] = topic
    pending_topic.discard(uid)
    # сразу разогрев по теме
    seed = f"Warm-up on topic: {topic}. Ask 1–2 engaging questions to start speaking."
    score = analyzer.polarity_scores(seed)["compound"]
    vad = fuse(text_sentiment=score, prosody_energy=None, vlm_label=None).tolist()
    answer = await tutor.reply(seed, vad, meta={"topic": topic, "kickoff": "warmup"})
    await m.answer(answer)

@dp.message(Command("cancel"))
async def cmd_cancel(m: Message):
    uid = m.from_user.id
    user_topics.pop(uid, None)
    pending_topic.discard(uid)
    await m.answer("Ок, отменил. На какую тему поговорим? (например: travel, coffee shop)")

@dp.message(Command("roleplay"))
async def cmd_roleplay(m: Message):
    uid = m.from_user.id
    topic = user_topics.get(uid)
    if not topic:
        pending_topic.add(uid)
        await m.answer("Сначала укажи тему: напиши её одним словом или используй /topic <тема>.")
        return
    seed = f"Let's start a short roleplay about: {topic}. You start."
    score = analyzer.polarity_scores(seed)["compound"]
    vad = fuse(text_sentiment=score, prosody_energy=None, vlm_label=None).tolist()
    answer = await tutor.reply(seed, vad, meta={"topic": topic, "force_roleplay": True})
    await m.answer(answer)

@dp.message(F.text)
async def on_text(m: Message):
    uid = m.from_user.id
    txt = m.text.strip()

    # если ждём тему — примем это сообщение как тему
    if uid in pending_topic or (uid not in user_topics and looks_like_topic(txt)):
        user_topics[uid] = txt
        pending_topic.discard(uid)
        seed = f"Warm-up on topic: {txt}. Ask 1–2 engaging questions to start speaking."
        score = analyzer.polarity_scores(seed)["compound"]
        vad = fuse(text_sentiment=score, prosody_energy=None, vlm_label=None).tolist()
        answer = await tutor.reply(seed, vad, meta={"topic": txt, "kickoff": "warmup"})
        await m.answer(f"Тема установлена: «{txt}».")
        await m.answer(answer)
        return

    topic = user_topics.get(uid)
    if not topic:
        pending_topic.add(uid)
        await m.reply("Сначала выберем тему. Напиши одним-двумя словами: *coffee shop*, *travel*, *job interview* …")
        return

    # обычный ход занятия: анализируем тональность и отвечаем
    score = analyzer.polarity_scores(txt)["compound"]  # [-1..1]
    vad = fuse(text_sentiment=score, prosody_energy=None, vlm_label=None).tolist()
    answer = await tutor.reply(txt, vad, meta={"topic": topic})
    await m.reply(answer)

async def main():
    if not Cfg.TG_TOKEN:
        raise RuntimeError("TG_BOT_TOKEN не найден. Создай .env в корне и укажи TG_BOT_TOKEN=...")
    from aiogram.types import BotCommand
    from aiogram.types import BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

    await bot.set_my_commands(
        commands=[
            BotCommand(command="start", description="Начни свой разговор с учителем!"),
            BotCommand(command="help", description="Подсказка"),
            BotCommand(command="topic", description="Задать тему разговора"),
            BotCommand(command="roleplay", description="Ролевая сцена"),
            BotCommand(command="cancel", description="Отмена шага"),
        ],
        scope=BotCommandScopeDefault(),  # глобально для всех чатов
        language_code="ru"  # локаль (можно убрать)
    )

    # (опционально) задать отдельно для личек и групп:
    await bot.set_my_commands([...], scope=BotCommandScopeAllPrivateChats(), language_code="ru")
    await bot.set_my_commands([...], scope=BotCommandScopeAllGroupChats(), language_code="ru")
    print("Bot started")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
