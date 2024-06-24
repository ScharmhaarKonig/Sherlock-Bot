import discord
import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()

# Function to perform reverse image search
def reverse_image_search(image_url, api_key, cx):
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': 'image search',
        'searchType': 'image',
        'imgUrl': image_url,
        'key': api_key,
        'cx': cx
    }
    response = requests.get(search_url, params=params)
    results = response.json()
    return results

# Replace with your own API key and CSE ID
api_key = os.getenv('API_KEY')
cx = os.getenv('219a4f32e801c42b2')

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/search'):
        # Extract the image URL from the message
        image_url = message.content[len('/search '):].strip()
        results = reverse_image_search(image_url, api_key, cx)
        
        response_message = ""
        
        if 'items' in results:
            items = results['items']
            response_message += f"Number of matches found: {len(items)}\n"
            for idx, item in enumerate(items):
                response_message += (f"{idx + 1}. Title: {item['title']}\n"
                                     f"   Link: {item['link']}\n"
                                     f"   Image: {item['image']['thumbnailLink']}\n"
                                     '---\n')
            if len(items) >= 3:
                response_message += 'Catfish alarm!\n'
            else:
                response_message += 'You\'re cool, just check for small details like email or social media.\n'
        else:
            response_message = 'No results found.'

        await message.channel.send(response_message)

# Run the bot with the token
client.run(os.getenv('DISCORD_TOKEN'))