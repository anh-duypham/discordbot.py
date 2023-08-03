import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import subprocess
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
@bot.command()
async def play(ctx, url):
    voice_channel = ctx.author.voice.channel
    if not voice_channel:
        await ctx.send("Vui lòng vào voice channel trước")
        return

    voice_client = ctx.voice_client
    if voice_client and voice_client.is_playing():
        await ctx.send("Bot đang phát nhạc")
        return

    try:
        if voice_client is None:
            await voice_channel.connect()
            voice_client = ctx.voice_client

        # Remove the old audio file if it exists
        if os.path.exists("audio.mp3"):
            os.remove("audio.mp3")

        command = f'yt-dlp "{url}" -x --audio-format mp3 -o "audio.mp3"'
        process = await asyncio.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            audio_file = "audio.mp3"
            voice_client.play(FFmpegPCMAudio(audio_file))
            await ctx.send("Đang phát nhạc...")
        else:
            await ctx.send("Không thể tải xuống âm thanh từ URL")

    except discord.ClientException:
        await ctx.send("Không thể kết nối vào voice channel")

    except Exception as e:
        await ctx.send(f"Có lỗi xảy ra: {str(e)}")
@bot.command()
async def skip(ctx):
    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.send("Bot không đang phát nhạc.")
        return

    if not voice_client.is_playing():
        await ctx.send("Không có nhạc đang phát.")
        return

    voice_client.stop()
    await ctx.send("Đã skip bài nhạc.")
    
    # Clear the downloaded audio file link
    os.remove("audio.mp3")
    
    # Disconnect the voice client to clear the audio source
    await voice_client.disconnect()
bot.run('INSERT YOUR TOKEN')
