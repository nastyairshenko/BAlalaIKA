import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, BotCommand
from aiogram.filters import Command, CommandStart

from src.core.config import Cfg
from src.tutor.virtual_tutor import VirtualTutor
from src.tutor.emotion_fusion import fuse
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
bot = Bot(Cfg.TG_TOKEN)
dp = Dispatcher()

# простая «память» тем по пользователям (в проде — БД/кэш)
user_topics: dict[int, str] = {}
# при желании можно хранить тут и по инстансу тьютора на пользователя
tutor = VirtualTutor()

# ---------- Команды ----------

@dp.message(CommandStart())
async def cmd_start(msg: Message):
    await msg.answer(
        "Привет! Я тьютор разговорного английского.\n"
        "Отправь /topic <тема> — о чём хочешь поговорить.\n"
        "Например: /topic travel to Japan"
    )

@dp.message(Command("help"))
async def cmd_help(msg: Message):
    await msg.answer(
        "/topic <тема> — задать тему разговора\n"
        "/roleplay — начать ролевую сцену по заданной теме\n"
        "/cancel — отменить текущий шаг\n"
        "Потом просто пиши сообщения — будем практиковаться 🙂"
    )

@dp.message(Command("topic"))
async def cmd_topic(msg: Message):
    # аргументы после названия команды
    args = msg.text.split(maxsplit=1)
    if len(args) == 1 or not args[1].strip():
        await msg.reply("Укажи тему: /topic job interview, /topic travel, /topic coffee shop …")
        return
    topic = args[1].strip()
    user_topics[msg.from_user.id] = topic
    await msg.answer(f"Тема установлена: «{topic}». Напиши сообщение — начнём разговор.")

@dp.message(Command("roleplay"))
async def cmd_roleplay(msg: Message):
    topic = user_topics.get(msg.from_user.id)
    if not topic:
        await msg.answer("Сначала задай тему: /topic <тема>")
        return
    seed = f"Let's start a short roleplay about: {topic}. You start."
    score = analyzer.polarity_scores(seed)["compound"]
    vad = fuse(text_sentiment=score, prosody_energy=None, vlm_label=None).tolist()

    answer = await tutor.reply(seed, vad, meta={"topic": topic, "force_roleplay": True})
    await msg.answer(answer)


@dp.message(Command("cancel"))
async def cmd_cancel(msg: Message):
    # минимальный сброс — только тема (при желании сбрасывайте и состояние тьютора)
    user_topics.pop(msg.from_user.id, None)
    await msg.answer("Отменил текущий шаг. Задай новую тему: /topic <тема>")

# ---------- Обычные сообщения ----------

@dp.message(F.text)
async def handle_text(msg: Message):
    # анализ тональности текста → Valence
    score = analyzer.polarity_scores(msg.text)["compound"]  # [-1..1]
    vad = fuse(text_sentiment=score, prosody_energy=None, vlm_label=None).tolist()

    topic = user_topics.get(msg.from_user.id)
    if not topic:
        await msg.reply("Сначала задай тему: /topic <тема>. Например: /topic coffee shop")
        return

    answer = await tutor.reply(msg.text, vad, meta={"topic": topic})
    await msg.reply(answer)

# ---------- Регистрация меню и запуск ----------

async def main():
    # Меню команд в Telegram (one source of truth — прямо в коде)
    await bot.set_my_commands([
        BotCommand(command="start",    description="Запуск и приветствие"),
        BotCommand(command="help",     description="Подсказка по командам"),
        BotCommand(command="topic",    description="Задать тему разговора"),
        BotCommand(command="roleplay", description="Ролевая сцена по теме"),
        BotCommand(command="cancel",   description="Отмена текущего шага"),
    ])
    print("Bot started")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
