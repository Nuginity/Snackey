import asyncio
from src.util import config

async def check_idle_and_disconnect(ctx, bot, idle_time=config['idle']):
    voice_client = ctx.voice_client
    if not voice_client:  # Pastikan bot sudah terhubung ke voice channel
        return

    # Periksa terus menerus selama bot ada di voice channel
    while voice_client.is_connected():
        if not voice_client.is_playing():  # Jika bot tidak memutar musik
            await asyncio.sleep(idle_time)  # Tunggu selama idle_time detik
            if not voice_client.is_playing():  # Jika masih tidak memutar musik
                await voice_client.disconnect()  # Keluar dari voice channel
                break  # Hentikan loop setelah disconnect
        await asyncio.sleep(1)  # Cek setiap 1 detik