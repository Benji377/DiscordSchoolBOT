import random
import re
import time
import discord
import asyncio
from discord.ext import commands
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from keep_alive import keep_alive
from textwrap import wrap

keep_alive()

bot = commands.Bot(command_prefix='<', activity=discord.Game(name="with you 😏"))
bot.remove_command("help")


### HELP SECTION ###
@bot.group(invoke_without_command=True)
async def help(ctx, dm_author:bool=False):
    em = discord.Embed(title="Help", description="Use <help <command> for extended information on that command\n"
                                                 "Parameters inside [] are optional, but <> are necessary",
                       color=ctx.author.color)
    em.add_field(name="General", value="ping, math")
    em.add_field(name="School", value="moodle_link, register")
    em.add_field(name="Fun", value="magicball, randnum")
    em.add_field(name="Malloc", value="malloc, storage, free")
    em.add_field(name="Others", value="greeting")
    em.set_footer(text="By Benben377 in collaboration with MacKenzie", icon_url="https://i.imgur.com/1VXg78F.jpeg")
    em.set_thumbnail(url="https://i.imgur.com/h9E67ko.png")

    await ctx.send(embed=em) if not dm_author else await ctx.author.send(embed=em)


@help.command()
async def ping(ctx):
    em = discord.Embed(title="Ping", description="Pings the Bot and returns a value in ms", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<ping")
    await ctx.send(embed=em)


@help.command()
async def moodle_link(ctx):
    em = discord.Embed(title="Moodle link", description="Logs in as guest to Moodle and scrapes the data from "
                                                        "the specified link", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<moodle_link <link>")
    await ctx.send(embed=em)


@help.command()
async def magicball(ctx):
    em = discord.Embed(title="Magicball", description="Answers yes-no questions (randomly)", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<magicball [question]")
    await ctx.send(embed=em)


@help.command()
async def randnum(ctx):
    em = discord.Embed(title="RandNum", description="Returns a random number between the two specified "
                                                    "min and max numbers", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<randnum <min> <max>")
    await ctx.send(embed=em)


@help.command()
async def greeting(ctx):
    em = discord.Embed(title="Greeting", description="Greets the specified user", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<greeting <user>")
    await ctx.send(embed=em)


@help.command()
async def malloc(ctx):
    em = discord.Embed(title="Malloc", description="Increases the storage randomly", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<malloc")
    await ctx.send(embed=em)


@help.command()
async def storage(ctx):
    em = discord.Embed(title="Storage", description="Returns the amount of storage", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<storage")
    await ctx.send(embed=em)


@help.command()
async def free(ctx):
    em = discord.Embed(title="Free", description="Frees up some storage randomly", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<free")
    await ctx.send(embed=em)


@help.command()
async def math(ctx):
    em = discord.Embed(title="Math", description="Does some simple math", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<math <expression>")
    await ctx.send(embed=em)


@help.command()
async def register(ctx):
    em = discord.Embed(title="Register", description="Gets a screenshot of the digital register "
                                                     "from homework section", color=ctx.author.color)
    em.add_field(name="**Syntax**", value="<register")
    await ctx.send(embed=em)


### FINISH ###

@bot.event
async def on_ready():
    print('Logged on as', bot.user)


@bot.command()
async def ping(ctx):
    await ctx.reply('Pong! {0} ms'.format(round(bot.latency * 1000, 1)))


@bot.command()
async def greeting(ctx, member: discord.Member):
    await ctx.reply("{0} says hello to {1} !".format(ctx.author.display_name, member.mention))


@bot.command()
async def moodle_link(ctx, message):
    async with ctx.channel.typing():
        await ctx.channel.send("Retrieving data...")
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        driver.get("https://moodle.tfobz.net/login/index.php")
        driver.find_element_by_id("guestlogin").click()
        driver.implicitly_wait(3)

        if "moodle" in message:
            driver.get(message)
            output = driver.find_element_by_class_name("no-overflow").text
            textfile = open('temp.txt', 'w')
            textfile.write(output)
            textfile.close()
            await ctx.reply(file=discord.File('temp.txt'))
            os.remove('temp.txt')
            driver.quit()
        else:
            output = "Not a moodle link"
            await ctx.reply(output)


@bot.command()
async def magicball(ctx):
    responses = [
        "It is certain",
        "Without a doubt",
        "You may rely on it",
        "Yes definitely",
        "It is decidedly so",
        "As I see it, yes",
        "Most likely",
        "Yes",
        "Outlook good",
        "Signs point to yes",
        "Reply hazy try again",
        "Better not tell you now",
        "Ask again later",
        "Cannot predict now",
        "Concentrate and ask again",
        "Don't count on it",
        "Outlook not so good",
        "My sources say no",
        "Very doubtful",
        "My reply is no",
        "No"
    ]
    answer = random.choice(responses)
    async with ctx.channel.typing():
        await asyncio.sleep(1)
        await ctx.reply(answer)


@bot.command()
async def randnum(ctx, *, message):
    max_min = re.findall(r"[-+]?\d*\.\d+|\d+", message)
    output = random.uniform(float(max_min[0]), float(max_min[1]))
    await ctx.reply(output)


@bot.event
async def on_message(message):
    if bot.user in message.mentions and message.author != bot.user:
        ctx = await bot.get_context(message)
        await message.channel.send('Hello {0}, check your DMs'.format(message.author.mention))
        await help(ctx, dm_author=True)
    call_words = ["sociality", "friend"]
    if any(call in message.content.lower() for call in call_words):
      await message.reply("Bot is active and ready for orders")
    zambo = ["zambo", "zambelli", "telezambo", "tele", "manuel"]
    if any(zambelli in message.content.lower() for zambelli in zambo):
        await message.reply("🤮")
    await bot.process_commands(message)



storage_space = 100


@bot.command()
async def malloc(ctx):
    global storage_space
    async with ctx.channel.typing():
        await ctx.channel.send("Storage is being prepared...")
        await asyncio.sleep(1)
        randomnum = random.randint(0, 500)
        storage_space += randomnum
        await ctx.channel.send("{0}MB storage added".format(randomnum))
        await ctx.channel.send("{0}MB total storage".format(storage_space))


@bot.command()
async def storage(ctx):
    global storage_space
    storage_string = str(storage_space)
    await ctx.channel.send("Total storage: {0}MB".format(storage_string))


@bot.command()
async def free(ctx):
    global storage_space
    async with ctx.channel.typing():
        await ctx.channel.send("Storage is being prepared...")
        await asyncio.sleep(1)
        randomnum = random.randint(0, 500)
        storage_space -= randomnum
        if storage_space <= 0:
            await ctx.channel.send("Tried to free {0}MB of storage".format(randomnum))
            await ctx.channel.send("Storage can't be freed anymore, storage = 0MB")
            storage_space = 0
        else:
            await ctx.channel.send("{0}MB storage freed".format(randomnum))
            await ctx.channel.send("{0}MB total storage".format(storage_space))


@bot.command()
async def math(ctx, *, message):
    async with ctx.channel.typing():
        await ctx.channel.send("Calculating...")
        await asyncio.sleep(2)
        try:
            result = eval(message)
            await ctx.channel.send("Result: {0}".format(result))
        except:
            await ctx.channel.send("Invalid expression")


@bot.command()
async def register(ctx):
    async with ctx.channel.typing():
        await ctx.channel.send("Retrieving data...")
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        driver.get('https://tfobz.digitalesregister.it/v2/login')
        driver.find_element_by_id('inputUserName').send_keys(os.getenv('USER'))
        driver.find_element_by_id('inputPassword').send_keys(os.getenv('PASSW'))

        driver.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(1)
        driver.get('https://tfobz.digitalesregister.it/v2/#vorstand/homework&klasse')
        time.sleep(1)
        driver.execute_script("window.scrollTo(0,500)")
        driver.save_screenshot('registerscreen.png')
        driver.quit()
        await ctx.channel.send(file=discord.File('registerscreen.png'))
        os.remove('registerscreen.png')
        await ctx.channel.send("End of file")


bot.run(os.getenv('TOKEN'))
