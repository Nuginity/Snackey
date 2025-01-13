import yt_dlp
import discord
import asyncio
import shutil
import os
from src.util import config

music_queue = []
cookies_file = 'cookies.txt'

def get_video_info(url):
    try:
        # Opsi untuk ydl (youtube-dl / yt-dlp)
        ydl_opts = {
            'cookiefile': cookies_file,  # Pastikan cookies_file sudah terdefinisi
            'format': 'bestaudio/best',  # Pilih format audio terbaik
            'noplaylist': True,           # Jangan download playlist
            'quiet': True,                # Menyembunyikan output yang tidak diperlukan
        }
        
        # Membuat instance yt_dlp dan mengambil informasi video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Mendapatkan informasi judul dan URL
            title = info.get('title', None)
            url2 = info.get('url', None)
            
            if title and url2:
                return title, url2
            else:
                print("Error: Unable to extract title or URL from the video.")
                return None, None
                
    except yt_dlp.DownloadError as e:
        print(f"Error downloading video: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
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