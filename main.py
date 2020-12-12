import discord
from discord.ext import commands
import requests
import aiohttp

TOKEN = "TOKEN BOT"

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    print('-------------------------')
    print('BOT - online')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('---------STATUS----------')

@client.command(pass_context=True)
async def post(ctx):
    em = discord.Embed(description=f"Loading...")
    msg = await ctx.send(embed=em)

    # Your message
    text = f"Your message | Sua mensagem"

    # Variables
    data = text
    link_hastebin = ''
    link_mystb = ''
    data = bytes(data, 'utf-8')

    # Create file in Hastebin.com
    async with aiohttp.ClientSession() as cs:
        async with cs.post('https://hastebin.com/documents', data=data) as r:
            res = await r.json()
            link_hastebin += f"https://hastebin.com/{(dict(res)['key'])}"

    # Create file in Mystb.in
    async with aiohttp.ClientSession() as cs:
        async with cs.post('https://mystb.in/documents', data=data) as r:
            res = await r.json()
            key = res["key"]
            link_mystb += f"https://mystb.in/{key}"

    # Create file in Pastebin.com
    key = 'your_key_account' # Get your token here https://pastebin.com/doc_api | search for: Your Unique Developer API Key
    t_title = "pastebin_title"
    login_data = {
        'api_dev_key': key,
        'api_user_name': 'your_username_login',
        'api_user_password': 'your_password_login'
    }
    data = {
        'api_option': 'paste', # paste | delete | list | userdetails | show_paste
        'api_dev_key': key,
        'api_paste_code': text,
        'api_paste_name': t_title,
        'api_paste_expire_date': '10M', # N = Never | 10M = 10 minutes | 1H = 1 hour | 1D = 1 day | 1W = 1 week | 2W = 2 weeks | 1M = 1 Mounth | 6M = 6 Months | 1Y = 1 Year
        'api_user_key': None,
        'api_paste_format': 'python' # python | C# | C | JSON | Lua ... More in: https://pastebin.com/doc_api
    }
    login = requests.post("https://pastebin.com/api/api_login.php", data=login_data)
    data['api_user_key'] = login.text
    link_pastebin = requests.post("https://pastebin.com/api/api_post.php", data=data)

    em = discord.Embed(title=f"",
                       description=f"**Hastebin:** {link_hastebin}\n"
                                   f"**Mystb:** {link_mystb}\n"
                                   f"**Pastebin:** {link_pastebin.text}")
    await msg.edit(embed=em)

client.run(TOKEN)