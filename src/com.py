from discord.ext import commands
import discord
from src.que import add_to_queue, play_next, show_queue, skip_current_song
from src.idle import check_idle_and_disconnect
from src.youtube_search import search_youtube
from discord.utils import get

current_volume = 1.0

# Membuat fungsi pembantu untuk memeriksa apakah bot terhubung ke voice channel
async def check_voice_client(ctx):
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You need to join a voice channel first!")
            return False
    return True

def setup(bot):
    @bot.command()
    async def stop(ctx):
        """Mengeluarkan bot dari voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I'm not in a voice channel!")

    @bot.command()
    async def play(ctx, *, query):
        """
        Mencari video di YouTube berdasarkan query dan memutarnya.
        """
        # Periksa apakah bot sudah di voice channel
        if not await check_voice_client(ctx):
            return

        # Cari video berdasarkan query
        video_url = search_youtube(query)
        if not video_url:
            await ctx.send("Tidak dapat menemukan video berdasarkan pencarian Anda.")
            return

        # Tambahkan video ke antrean
        await add_to_queue(ctx, video_url)

        # Jika bot tidak sedang memutar musik, mulai memutar
        if not ctx.voice_client.is_playing():
            await play_next(ctx, bot)

        bot.loop.create_task(check_idle_and_disconnect(ctx, bot))

    @bot.command()
    async def antrian(ctx):
        """Menampilkan daftar antrean lagu."""
        await show_queue(ctx)

    @bot.command()
    async def skip(ctx):
        """Melewati lagu saat ini."""
        await skip_current_song(ctx)

    @bot.command()
    async def volume(ctx, volume: float):
        """
        Mengubah volume bot berdasarkan persentase (0-100).
        volume: float - Persentase volume (0 - 100)
        """
        voice = get(ctx.bot.voice_clients, guild=ctx.guild)  # Mendapatkan voice client

        # Pastikan volume berada di antara 0 dan 100
        if 0 <= volume <= 100:
            if voice and voice.is_playing():  # Cek apakah bot terhubung dan sedang memutar sesuatu
                new_volume = volume / 100  # Ubah volume ke range 0.0 - 1.0
                voice.source.volume = new_volume  # Set volume pada source yang sedang diputar
                await ctx.send(f"Volume telah diatur ke {volume}%.")
            else:
                await ctx.send("Bot tidak sedang memutar suara atau tidak terhubung ke voice channel.")
        else:
            await ctx.send("Volume harus berada di antara 0 dan 100.")