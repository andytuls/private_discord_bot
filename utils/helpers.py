import discord

def progress_bar(current: int, total: int, length: int = 10) -> str:
    if total == 0:
        return "█" * length
    filled = int(round((current / total) * length))
    empty = length - filled
    return "█" * filled + "░" * empty

HELP_DATA = {
    "главная": {
        "title": "📚 Справка по боту",
        "description": "Здрвствуй. Я Валентин. Выберите раздел ниже, чтобы узнать необходимую информацию.",
        "sections": ["основные", "игровые"]
    },
    "основные": {
        "title": "⚙️ Основные команды",
        "description": "Команды для управления ботом и получения информации.",
        "commands": [
            {"name": "!привет", "desc": "Поздороваться с Валентином"},
            {"name": "!пинг", "desc": "Проверить задержку Валентина"},
            {"name": "!справка", "desc": "Эм, ты ведь понимаешь, зачем это?"},
            {"name": "!повтори", "desc": "Попросить Валентина повторить свои слова"},
            {"name": "!свечи", "desc": "Показывает количество свечек у пользователя"},
            {"name": "!топ", "desc": "Показывает топ пользователей по свечкам"}
        ]
    },
    "игровые": {
        "title": "🎲 Игровые команды",
        "description": "Команды для игры в слова и не только.",
        "commands": [
            {"name": "!шанс", "desc": "Сделать бросок кости. 1 аргумент-количество граней, 2-количество костей.\n Можно сделать выбор между несколькими вариантами, разделёнными запятой."},
            {"name": "!слова", "desc": "Показать статистику игры в слова"},
            {"name": "!буква", "desc": "Показать статистику по букве"},
            {"name": "!подсказка", "desc": "Валентин подсказывает слово на текущую букву"},
            {"name": "!перезапуск_слов", "desc": "Стирает данные об игре в слова. Админ команда"},
            {"name": "!дс", "desc": "Добавляет слова в словарь для игры. Админ команда"}
        ]
    }
}

MILESTONE_MESSAGES = {
    10: {
        "message": "Твой путь, {user}, только начинается... Ты достиг {count} свечек. 🕯️"
    },
    42: {
        "message": "Каков ответ на все вопросы? {user} достиг {count} свечек 🕯️"
    },
    69: {
        "message": "{user} достиг {count} свечек! 🕯️"
    },
    100: {
        "message": "{user} заслуживает увжаения со своей {count} свечек. Обратись к Барашу для получения секретного приза. 🕯️🌟"
    },
    220: {
        "message": "КАТАСТРОФА! {user} достиг {count} свечек! 🕯️"
    },
    420: {
        "message": "Отдохни, братишка! {user} достиг {count} СВЕЧЕК 🕯️"
    },
    666: {
        "message": "Сатана гордится. {user} достиг {count} свечек! 🕯️"
    },
    777: {
        "message": "Повезло! {user} достиг {count} свечек! 🕯️"
    },
    1000: {
        "message": "Твой путь был легендарен.  {user} покорил {count} свечек 🕯️👑. Обратись к Барашу для получения секретного приза."
    },
    "multiple_of_100": {
        "message": "Новый рубеж. {user} достиг {count} свечек! 🕯️"
    }
}

def generate_embed(section_key: str) -> discord.Embed:
    section = HELP_DATA[section_key]
    embed = discord.Embed(
        title=section["title"],
        description=section.get("description", ""),
        color=discord.Color.blue()
    )

    if "commands" in section:
        for cmd in section["commands"]:
            embed.add_field(
                name=cmd["name"],
                value=cmd["desc"],
                inline=False
            )

    return embed