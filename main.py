import discord
import os 
from dotenv import load_dotenv
import requests
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    data = response.json()[0]
    quote = data['q'] + ' \n- ' + data['a']
    return quote

def get_meme():
    response = requests.get("https://api.imgflip.com/get_memes")
    data = response.json()
    memes = data['data']['memes']
    meme = random.choice(memes)
    return meme
def get_weather():
    load_dotenv()
    BASE_URL = os.getenv('BASE_URL')
    API_KEY = os.getenv('API_KEY')
    CITY =  os.getenv('CITY')
    url = BASE_URL +  "appid=" + API_KEY + "&q=" + CITY
    response = requests.get(url).json()
    temp_kelvin = response["main"]["temp"]
    temp_celsius = str(round(int(temp_kelvin)-273.15,2))
    feels_like_kelvin = response["main"]["feels_like"]
    feels_like_celsius = str(round(int(feels_like_kelvin)-273.15,2))
    description = response["weather"][0]["description"]
    result = f"Current temperature:{temp_celsius}°C" + "\n" + f"Feels like: {feels_like_celsius}°C" +"\n" + f"{description}"
    return result

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if "$how are you" in message.content.lower():
        await message.channel.send("I'm great! How are you?")
    if "$inspire" in message.content.lower():
        quote = get_quote()
        await message.channel.send(quote)
    if "$weather" in message.content.lower():
        weather = get_weather()
        await message.channel.send(weather)
    if "$meme" in message.content.lower():
        meme = get_meme()
        embed = discord.Embed(title=meme['name'])
        embed.set_image(url=meme['url'])
        await message.channel.send(embed=embed)

load_dotenv()
client.run(os.getenv('TOKEN'))
