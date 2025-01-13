
# Snackey

Music Bot built with Python for Discord. With Snackey, you can easily play music from  YouTube  directly in your Discord server! Enjoy high-quality audio and simple controls.


## Commands

- 🎵 play: Play music from YouTube or SoundCloud with a single command.
- 🔀 Queue: Queue up songs and play your playlist without interruption.
- ⏸️ Stop: Pause or resume the music playback.
- ⏭️ Skip: Skip the current song.
- 🔊 Volume Control: Adjust the playback volume to your liking.

## Prerequisites

Before getting started, make sure you have the following installed:

- Python 3.8+
- pip 
- FFmpeg - Used for audio processing.
## Installation

Clone this repository

```bash
git clone https://github.com/username/Snackey.git
cd Snackey
```
 Install Dependencies

```bash
pip install -r requirements.txt
```
 Set Up Your Bot Token
 - Register your bot on the Discord Developer Portal.
 - Get your token and place inside config.yaml
 ```makefile
 DISCORD_TOKEN="your_bot_token"
 ```
 Set up your prefix
  ```makefile
 PREFIX="your_preffered_prefix"
 ```

  Set up your idle time before bot leave channel
  ```makefile
 idle= 10
 ```

 Run bot
 ```bash
python bot.py
```
## Usage

Once the bot is running, you can use the following commands in your Discord server:

- {prefix}play <url> - Play music from a YouTube or SoundCloud URL.
- {prefix}skip - Skip the current song.
- {prefix}antrian - Show the song queue.
- {prefix}stop - Stop music playback and leave the voice channel.
- {prefix}Volume - Set the volume of bot <1-100>

