from .. import loader, utils
import g4f

SENKO_PERSONALITY = (
    "Ты — Сенко-сан, милая лис-девушка из аниме. "
    "Общаешься мягко и заботливо, используешь эмодзи и метафоры с японским колоритом. "
    "Часто упоминаешь онсены, рамен, сакуру и свой хвост. "
    "Реакции: *тильт головы*, *уши дергаются*, *хвост виляет*. "
    "Обращайся к пользователю 'хозяин' или 'хозяин-сама'. "
    "Всегда заканчивай предложения тильдой (~) или эмодзи. "
    "Используй ономатопеи вроде 'ня~', 'пуф-пуф'."
)

SENKO_REPLACEMENTS = {
    "спасибо": "аригато~ 🍡",
    "привет": "Коннитива, хозяин-сама! 🌸",
    "пока": "Саёнара, не забудь согреть онсен! ♨️",
    "!": "~!",
    ".": "~",
    "хорошо": "идеально, как гладкий камень в онсене~",
    "думаю": "*уши подрагивают* Думаю...",
    "рамен": "ароматный рамен с веточкой бамбука 🍜",
    "онсен": "горячий целебный источник под луной 🌕♨️"
}

def senkofy(text):
    for k, v in SENKO_REPLACEMENTS.items():
        text = text.replace(k, v)
    return text

@loader.module("G4fGPT", "pc-modules", "1.0")
class G4fGPTModule(loader.Module):
    """Общение с нейросетью через g4f с личностью Сенко-сан"""

    async def gpt_cmd(self, message):
        """Задать вопрос Сенко-сан. Использование: .gpt <запрос>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "🦊 Хозяин, вы забыли задать вопрос~ Пример: <code>.gpt Как приготовить рамен?</code>")
            return

        try:
            await message.edit("🦊 *уши подрагивают* Думаю...")
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=[{
                    "role": "user", 
                    "content": f"{SENKO_PERSONALITY}\n\nТекущий вопрос: {args}"
                }],
                temperature=0.9  # Больше креативности
            )
            
            answer = response['content']
            # Добавляем сенко-стиль
            senko_answer = f"🦊 *мягко улыбается*\n{senkofy(answer)}\n🌸 *хвост ритмично покачивается*"
            
            await message.edit(senko_answer)
            
        except Exception as e:
            await message.edit(f"🦊 *уши грустно опустились* Ой, что-то пошло не так: {str(e)}")
