import yt_dlp
import discord
import asyncio
import shutil
import os
from src.util import config

music_queue = []

def get_video_info(url):
    """Mendapatkan informasi dari video dengan URL yang diberikan."""
    cookies_file = "cookies.txt"  # Jalur file cookies

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': False,  # Aktifkan log untuk debugging
        'noplaylist': True,
    }

    if os.path.exists(cookies_file):
        ydl_opts['cookiefile'] = cookies_file
        print(f"Menggunakan cookies dari: {cookies_file}")
    else:
        print("File cookies.txt tidak ditemukan, melanjutkan tanpa cookies.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            return title, info['url']
    except Exception as e:
        print(f"Error saat mendownload atau mencari video: {e}")
        return None, None

def get_ffmpeg_path():
    """Mencari lokasi ffmpeg secara otomatis di sistem."""
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    else:
        if os.name == 'nt':
            return config['FF-PATH'][0]
        elif os.name == 'posix':
            return config['FF-PATH'][1]
        else:
            raise EnvironmentError("ffmpeg tidak ditemukan dan sistem operasi tidak didukung")

async def add_to_queue(ctx, url):
    """Menambahkan lagu ke antrean."""
    music_queue.append(url)

async def play_next(ctx, bot):
    """Memutar lagu berikutnya dari antrean."""
    if music_queue:
        url = music_queue.pop(0)
        vc = ctx.voice_client

        title, url2 = get_video_info(url)
        if not url2:
            await ctx.send("Terjadi kesalahan saat memutar video.")
            return

        def after_playing(error):
            if error:
                print(f"Error during playback: {error}")
            asyncio.run_coroutine_threadsafe(play_next(ctx, bot), bot.loop)

        ffmpeg_path = get_ffmpeg_path()

        audio_source = discord.FFmpegPCMAudio(url2, executable=ffmpeg_path)
        vc.play(discord.PCMVolumeTransformer(audio_source), after=after_playing)
        await ctx.send(f"Sekarang memutar: {title}")

async def show_queue(ctx):
    """Menampilkan antrean lagu dengan judul dari antrian pertama."""
    if music_queue:    
        pesan_antrean = "Daftar antrean:\n"
        
        for i, url in enumerate(music_queue):
            title, _ = get_video_info(url) 
            pesan_antrean += f"{str(i+1)}. **{title}**\n"
        
        await ctx.send(pesan_antrean)
    else:
        await ctx.send("Antrean kosong!")

async def skip_current_song(ctx):
    """Melewati lagu yang sedang diputar."""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Melewati lagu ini!")
    else:
        await ctx.send("Tidak ada lagu yang sedang diputar!")