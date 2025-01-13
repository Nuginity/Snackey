import yt_dlp
import discord
import asyncio

# Variabel global untuk antrean musik
music_queue = []

# Fungsi untuk mendapatkan informasi video dari YouTube
def get_video_info(url):
    """Mendapatkan informasi dari video dengan URL yang diberikan."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            return title, info['url']
    except Exception as e:
        print(f"Error saat mendapatkan informasi video: {e}")
        return None, None

async def add_to_queue(ctx, url):
    """Menambahkan lagu ke antrean."""
    music_queue.append(url)

async def play_next(ctx, bot):
    """Memutar lagu berikutnya dari antrean."""
    if music_queue:
        url = music_queue.pop(0)
        vc = ctx.voice_client

        # Dapatkan informasi video
        title, url2 = get_video_info(url)
        if not url2:
            await ctx.send("Terjadi kesalahan saat memutar video.")
            return

        # Fungsi untuk dijalankan setelah lagu selesai
        def after_playing(error):
            if error:
                print(f"Error during playback: {error}")
            asyncio.run_coroutine_threadsafe(play_next(ctx, bot), bot.loop)

        # Putar audio
        ffmpeg_path = "C:/Alat/ffmpeg/bin/ffmpeg.exe"
        audio_source = discord.FFmpegPCMAudio(url2, executable=ffmpeg_path)
        vc.play(discord.PCMVolumeTransformer(audio_source), after=after_playing)
        await ctx.send(f"Sekarang memutar: {title}")

async def show_queue(ctx):
    """Menampilkan antrean lagu dengan judul dari antrian pertama."""
    if music_queue:
        # Buat pesan antrean
        pesan_antrean = "Daftar antrean:\n"
        
        # Ambil informasi dari semua video dalam antrean
        for i, url in enumerate(music_queue):
            title, _ = get_video_info(url)  # Ambil hanya judul
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