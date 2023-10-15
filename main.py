import discord
import sys
import time
import datetime
from discord.ext import commands
from music import call_AudD

f = open("token.txt", "r")
TOKEN = f.read()
f.close()

backslash = "/"
currentDateAndTime = time.localtime()
currentTime = time.strftime("%H:%M", currentDateAndTime)
logName = f"{datetime.date.today()}:{currentTime}"
logFileName = logName.replace(":", "-")

acceptedFileTypes = ["audio/mpeg" ,"audio/ogg", "video/mp4"]

sys.stdout = open(f"%appdata%/auddiscord/logs/{logFileName}.log", "w")


Emoji = "musical_note"
newline = "\n"
intents = discord.Intents.all()
client = commands.Bot(command_prefix="!!", intents = intents, help_command=None)

@client.event
async def on_ready():
    print("Bot is running")
    await client.change_presence(status=discord.Status.online)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="uhhhhhhuhhh"))


@client.event
async def on_message(message):
    try:
        if message.reference != None and client.user.mentioned_in(message):
            channel = message.channel
            msg = await channel.fetch_message(message.reference.message_id)

            if msg.attachments != None and msg.attachments[0].content_type in acceptedFileTypes:
                at = msg.attachments[0]
                artist, title, album, songUrl, artistUrl, imageLink = call_AudD(at)
                embed=discord.Embed(title=title, url=songUrl, description=f"{newline}**Album**{newline}{album}")
                embed.set_author(name=f"Artist: {artist}", url=artistUrl)
                embed.set_thumbnail(url=imageLink)
                embed.set_footer(text="Provided by the AudD API.")
                await message.channel.send(embed=embed)
                

            elif msg.attachments != None and msg.attachments[0].content_type not in acceptedFileTypes:
                await message.channel.send("Unsupported filetype!")

            elif message.embeds.video.url != None:
                at = message.embeds.video.url

            else:
                await message.channel.send("This message doesnt have any attachments!")

        await client.process_commands(message)

    except IndexError:
        await message.channel.send("No attachments!")
        await client.process_commands(message)

    except Exception as E:
        await message.channel.send("ERROR:" + sys.exc_info()[0])
        await client.process_commands(message)
        print(f"Exception {e} Occured at {currentTime}")


@client.event
async def on_raw_reaction_add(message):
    try:
        channel = client.get_channel(message.channel_id)
        msg = await channel.fetch_message(message.message_id)

        if Emoji in message.emoji.name and msg.attachments != None and msg.attachments[0].content_type in acceptedFileTypes:
            at = msg.attachments[0]
            artist, title, album, songUrl, artistUrl, imageLink = call_AudD(at)
            embed=discord.Embed(title=title, url=songUrl, description=f"{newline}**Album**{newline}{album}")
            embed.set_author(name=f"Artist: {artist}", url=artistUrl)
            embed.set_thumbnail(url=imageLink)
            embed.set_footer(text="Provided by the AudD API.")
            await msg.channel.send(embed=embed)

        elif msg.attachments != None and msg.attachments[0].content_type not in acceptedFileTypes:
            await message.channel.send("Unsupported filetype!")

        elif Emoji in msg.reactions and msg.attachments is None:
            await message.channel.send("This message doesnt have any attachments!")

    except IndexError:
        await message.channel.send("No attachments!")

    except Exception as e:
        await message.channel.send("Something went wrong!")
        print(f"Exception {e} Occured at {currentTime}")

@client.command()
async def songcheck(ctx):
    try:
        msg = await ctx.channel.fetch_message(ctx.message.message_id)
        if ctx.message.attachments != None and ctx.message.attachments[0].content_type in acceptedFileTypes:
            at = ctx.message.attachments[0]
            artist, title, album, songUrl, artistUrl, imageLink = call_AudD(at)
            embed=discord.Embed(title=title, url=songUrl, description=f"{newline}**Album**{newline}{album}")
            embed.set_author(name=f"Artist: {artist}", url=artistUrl)
            embed.set_thumbnail(url=imageLink)
            embed.set_footer(text="Provided by the AudD API.")
            await ctx.send(embed=embed)

        elif msg.attachments != None and msg.attachments[0].content_type not in acceptedFileTypes:
            await ctx.send("Unsupported filetype!")

    except IndexError:
        await ctx.send("This message has no attachments!")

    except:
      await ctx.send("An error occurred")


@client.command()
async def help(ctx):
    embedHelp=discord.Embed(title=f"{newline}", description=f"This bot uses '!!' as its prefix. {newline}{newline} Use !!songcheck and attach a file or link, react to an upload with :musical_note:, or reply to a message that has a file and ping me to figure out what damn music they use for all the videos you see.")
    embedHelp.set_author(name="Help!")
    embedHelp.set_footer(text="Provided by the AudD API.")
    await ctx.send(embed=embedHelp)


client.run(TOKEN)    
