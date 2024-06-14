
import discord
import os
import requests
import io
from discord.ext import commands
from discord.utils import get
import replicate
import subprocess
from dotenv import load_dotenv
from temp import generate_and_display_image
load_dotenv()



CAT_API_KEY = os.getenv("CAT_API_KEY")
DOG_API_URL = os.getenv("DOG_API_URL")
TOKEN = os.getenv("TOKEN")

class MyClient(commands.Bot):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            # channel = message.channel
            
            channel = message.channel
            image_bytes = generate_and_display_image(message.content)
            if(image_bytes==None):
                 await channel.send("Couldn't fetch an image at the moment. Please try again later.")
                 return
            else:
                await channel.send(file=discord.File(io.BytesIO(image_bytes), 'generated_image.jpg'))



            

        if 'cat' in message.content.lower() or 'cats' in message.content.lower():
            await self.send_cat_image(message.channel)

        if 'dog' in message.content.lower() or 'dogs' in message.content.lower():
            await self.send_dog_image(message.channel)


    async def send_cat_image(self, channel):
        cat_api_url = f'https://api.thecatapi.com/v1/images/search?api_key={CAT_API_KEY}&format=json'
        try:
            response = requests.get(cat_api_url)
            data = response.json()

            if response.status_code == 200 and data:
                cat_image_url = data[0]['url']
                cat_image = requests.get(cat_image_url).content
                await channel.send(file=discord.File(io.BytesIO(cat_image), 'cat.jpg'))
            else:
                await channel.send("Couldn't fetch a cat image at the moment. Please try again later.")
        except Exception as e:
            print(f"Error fetching cat image: {e}")
            await channel.send("An error occurred while fetching a cat image. Please try again later.")

    async def send_dog_image(self, channel):
        try:
            response = requests.get(DOG_API_URL)
            data = response.json()

            if response.status_code == 200 and data['status'] == 'success':
                dog_image_url = data['message']
                dog_image = requests.get(dog_image_url).content
                await channel.send(file=discord.File(io.BytesIO(dog_image), 'dog.jpg'))
            else:
                await channel.send("Couldn't fetch a dog image at the moment. Please try again later.")
        except Exception as e:
            print(f"Error fetching dog image: {e}")
            await channel.send("An error occurred while fetching a dog image. Please try again later.")



