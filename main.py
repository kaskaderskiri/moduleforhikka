from hikka import loader, utils
from g4f import ChatCompletion, Provider

@loader.tds
class GPTModule(loader.Module):
    """Генерация текста через GPT с использованием g4f"""
    
    strings = {
        "name": "GPTModule",
        "processing": "<b>🌀 Обрабатываю запрос...</b>",
        "error": "<b>❌ Ошибка генерации</b>"
    }

    async def gptcmd(self, message):
        """<запрос> - Сгенерировать текст с помощью GPT"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>❌ Укажите текст запроса</b>")
            return

        try:
            m = await message.edit(self.strings("processing"))
            response = await utils.run_in_executor(
                ChatCompletion.create_async,
                model="gpt-3.5-turbo",
                provider=Provider.Bing,
                messages=[{"role": "user", "content": args}],
                stream=False
            )
            await m.edit(f"<b>🤖 Ответ:</b>\n{response}")
        except Exception as e:
            await message.edit(f"{self.strings('error')}: {str(e)}")