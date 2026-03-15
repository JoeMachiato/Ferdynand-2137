import discord
from discord.ext import tasks
import datetime
import zoneinfo
import asyncio
import yt_dlp
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
TEXT_CHANNEL_ID = int(os.getenv("TEXT_CHANNEL_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))
ROLE_ID = os.getenv("ROLE_ID")

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
    'quiet': True,
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ss 27 -t 60'
}

class Ferdynand(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.daily_message.start()

    async def on_ready(self):
        print(f'Zalogowano jako {self.user}')

    tz_poland = zoneinfo.ZoneInfo("Europe/Warsaw")
    
    @tasks.loop(time=datetime.time(hour=21, minute=37, tzinfo=tz_poland))
    async def daily_message(self):
        text_channel = self.get_channel(TEXT_CHANNEL_ID)
        voice_channel = self.get_channel(VOICE_CHANNEL_ID)
        
        if text_channel:
            message = f"<@&{ROLE_ID}> WYBIŁA PAPIEŻOWA 2137!"
            for i in range(3):
                await text_channel.send(message, allowed_mentions=discord.AllowedMentions(everyone=True))

        if voice_channel and isinstance(voice_channel, discord.VoiceChannel):
            vc = await voice_channel.connect()
            
            song_url = "https://www.youtube.com/watch?v=2yusdx60_aw"
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song_url, download=False)
                audio_stream_url = info['url']
                
            source = discord.FFmpegPCMAudio(audio_stream_url, **ffmpeg_options)
            vc.play(source)
            
            while vc.is_playing():
                await asyncio.sleep(1)
                
            await vc.disconnect()

intents = discord.Intents.default()
client = Ferdynand(intents=intents)

client.run(TOKEN)