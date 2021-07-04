import os, json, codecs # for importing env vars for the bot to use
from twitchio.ext import commands

stores = ['coolmod', 'pccomponentes', 'vsgamers', 'neobyte', 'aussar', 'siabyte', 'lifeinformatica', 'izarmicro']

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    await bot.handle_commands(ctx)

def getLink(id):
    with open('../../source.json', 'r') as jsonFile:
        data = json.load(jsonFile)
        for item in data:
            if item['id']==id:
                if 'addToCart' in item and item['status'] == 'IN STOCK':
                    return item['addToCart']
                else:
                    return item['url']
        return "-1"

@bot.command(name='link')
async def link(ctx):
    if (len(ctx.content.lower())>0 and len(ctx.content.lower().split())>1):
        link = getLink(ctx.content.lower().split()[1])
        if link != '-1':
            await ctx.channel.send(f"@{ctx.author.name} aquí lo tienes! " + link)
        else:
            await ctx.channel.send(f"@{ctx.author.name} no he encontrado ese id! asegurate de poner el número que aparece en amarillo con el formato: !link 123")
    else:
        await ctx.channel.send(f"@{ctx.author.name} asegurate de pedir el link con el formato: !link 123 ")

def saveLink(link):
   text_file = codecs.open("links.txt", "a+", "utf-8")
   text_file.write(link + '\n')
   text_file.close()

@bot.command(name='add')
async def add(ctx):
    if (len(ctx.content.lower())>0 and len(ctx.content.lower().split())==2) and ctx.content.lower().split()[1].startswith('http'):
        link = ctx.content.lower().split()[1]
        if any(store in link for store in stores):
            saveLink(link)
            await ctx.channel.send(f"@{ctx.author.name} tomo nota! Lo revisaré y añadiré cuanto antes!")
        else:
            await ctx.channel.send(f"@{ctx.author.name} todavía no soportamos esa tienda, asegúrate que el link lleva a un producto de una de las siguientes tiendas: coolmod, pccomponentes, vsgamers, neobyte, aussar, siabyte, lifeinformatica o izarmicro")
    else:
        await ctx.channel.send(f"@{ctx.author.name} asegurate de pasarme el link con el formato: !add http...")

if __name__ == "__main__":
    bot.run()