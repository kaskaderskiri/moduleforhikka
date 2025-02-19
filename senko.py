# _  __         _             _                 _    _      _ 
# | |/ /__ _ ___| | ____ _  __| | ___ _ __   ___| | _(_)_ __(_)
# | ' // _` / __| |/ / _` |/ _` |/ _ \ '__| / __| |/ / | '__| |
# | . \ (_| \__ \   < (_| | (_| |  __/ |    \__ \   <| | |  | |
# |_|\_\__,_|___/_|\_\__,_|\__,_|\___|_|    |___/_|\_\_|_|  |_|
#                                                         by kaskader skiri    
#
#
#            _              _ _   _                                    
#  __ _ _ __ | |_  __      _(_) |_| |__                                 
# / _` | '_ \| __| \ \ /\ / / | __| '_ \                                
#| (_| | |_) | |_   \ V  V /| | |_| | | |                               
# \__, | .__/ \__|   \_/\_/ |_|\__|_| |_|              _         _      
#  |___/|_| _ __ | | _____        ___  __ _ _ __    ___| |_ _   _| | ___ 
# / __|/ _ \ '_ \| |/ / _ \ _____/ __|/ _` | '_ \  / __| __| | | | |/ _ \
# \__ \  __/ | | |   < (_) |_____\__ \ (_| | | | | \__ \ |_| |_| | |  __/
# |___/\___|_| |_|_|\_\___/      |___/\__,_|_| |_| |___/\__|\__, |_|\___|
#                                                          |___/        

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: GigaChat
# Description: GigaChat AI. БЕЗ АПИ, отвечающий как Сенко-Сан из манги Sewayaki no kitsune senko-san
# meta developer @kaskaderskiri
# requires: aiohttp
# ---------------------------------------------------------------------------------

import asyncio
import logging
import hikkatl

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class GigaChat(loader.Module):
    """GigaChat AI. БЕЗ АПИ"""

    strings = {
        "name": "🦊 Senko-San Care",

        "no_args": "❌🦊 <b>Нужно </b><code>{}{} {}</code>",

        "asking_gg": "🔄🍡 <b>Спрашиваю Сенко-сан...</b>",

        "answer": """{answer}

❓🍙 <b>Вопрос:</b> {question}""",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.ggbot = "@GigaChat_Bot"

        try:
            async with self._client.conversation(self.ggbot) as conv:
                msg = await conv.send_message("/start")
                r = await conv.get_response()
                await msg.delete()
                await r.delete()
        except:
            pass

    async def _ask_ai(self, q):
        while True:
            try:
                async with self._client.conversation(self.ggbot) as conv:
                    msg = await conv.send_message(q)
                    r = await conv.get_response()
                    await msg.delete()
                    await r.delete()
                return r.text
            except hikkatl.errors.common.AlreadyInConversationError:
                await asyncio.sleep(5.67)

    @loader.command()
    async def senko(self, message):
        """Попросить Сенко-сан о помощи"""
        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_args"].format(
                self.get_prefix(), 
                "senko",  # Меняем название команды здесь
                "[ваш вопрос]"
            ))

        await utils.answer(message, self.strings['asking_gg'])

        return await utils.answer(
            message,
            self.strings['answer'].format(
                question=q, 
                answer=await self._ask_ai(q))
            )