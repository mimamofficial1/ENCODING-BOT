import asyncio

import dns.resolver
from pyrogram import idle
from pyrogram.errors import FloodWait

from . import app, log, LOGGER

dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = [
    '8.8.8.8']  # this is a google public dns


async def main():
    # FloodWait aaye toh crash hone ke bajay wait karke dobara login try karo
    while True:
        try:
            await app.start()
            break
        except FloodWait as e:
            wait = e.value + 5
            LOGGER.warning(f'FloodWait on login, sleeping {wait}s before retry')
            await asyncio.sleep(wait)

    # Log channel galat ho toh bhi bot band na ho
    try:
        await app.send_message(chat_id=log, text=f'<b>Bot Started! @{(await app.get_me()).username}</b>')
    except Exception as e:
        LOGGER.error(f'Startup message send nahi hua (LOG_CHANNEL check karo): {e}')

    await idle()
    await app.stop()

app.loop.run_until_complete(main())
