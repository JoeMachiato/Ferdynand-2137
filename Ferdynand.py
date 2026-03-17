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

def findBestChannel(guild):
    best_channel = None
    most_people = 0

    for channel in guild.voice_channels:
        real_members = [member for member in channel.members if not member.bot]
        liczba_osob = len(real_members)

        if liczba_osob > most_people:
            most_people = liczba_osob
            best_channel = channel

    return best_channel

class Ferdynand(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        self.daily_message.start()

    async def on_ready(self):
        print(f'Zalogowano jako {self.user}')

    tz_poland = zoneinfo.ZoneInfo("Europe/Warsaw")
    
    @tasks.loop(time=datetime.time(hour=21, minute=37, second=5, tzinfo=tz_poland))
    async def daily_message(self):
        text_channel = self.get_channel(TEXT_CHANNEL_ID)
        fallback_voice_channel = self.get_channel(VOICE_CHANNEL_ID)
        
        if text_channel:
            message = f"<@&{ROLE_ID}> WYBIŁA PAPIEŻOWA 2137!"
            for i in range(3):
                await text_channel.send(message, allowed_mentions=discord.AllowedMentions(everyone=True))

        target_voice_channel = None
        guild = None
        
        if fallback_voice_channel:
            guild = fallback_voice_channel.guild
        elif text_channel:
            guild = text_channel.guild

        if guild:
            target_voice_channel = findBestChannel(guild)

        if target_voice_channel is None:
            target_voice_channel = fallback_voice_channel

        if target_voice_channel and isinstance(target_voice_channel, discord.VoiceChannel):
            vc = await target_voice_channel.connect()
            
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
intents.members = True

client = Ferdynand(intents=intents)
client.run(TOKEN)