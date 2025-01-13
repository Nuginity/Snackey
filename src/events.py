def setup(bot):
    @bot.event
    async def on_ready():
        """Event ketika bot berhasil terhubung ke Discord."""
        print(f"Logged in as {bot.user}")

    @bot.event
    async def on_message(message):
        """Event ketika bot menerima pesan."""

        # Jangan merespons pesan dari bot lain (termasuk bot ini)
        if message.author.bot:
            return

        # Pastikan command handler tetap berjalan
        await bot.process_commands(message)