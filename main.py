import discord
from discord.ext import commands
from config import TOKEN, API_KEY
import aiohttp
import openai
from io import BytesIO
from PIL import Image

openai.api_key = API_KEY

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot connected to Discord!")


@bot.command()
async def sota(ctx: commands.Context, *, prompt: str):
    print(prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    await ctx.send(content=response["choices"][0]["message"].content)


@bot.command()
async def sotaimg(ctx: commands.Context, *, prompt: str):
    print(prompt)
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    await ctx.send(image_url)


@bot.command()
async def sotamod(ctx: commands.Context):
    try:
        img: Image
        if len(ctx.message.attachments) > 0:
            if len(ctx.message.attachments) != 1:
                await ctx.send(
                    content="Debes enviarme solo una imagen, no puedo hacer la pega si me mandas más o menos de una imagen.")
                return

            attachment = ctx.message.attachments[0]
            # Descargar archivo adjunto
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as response:
                    if response.status == 200:
                        image_bytes = await response.read()
                        with open('imgs/modify.png', 'wb') as f:
                            f.write(image_bytes)
                    else:
                        await ctx.send(
                            content="Lo siento, no pude leer la imagen correctamente bro, intentalo denuevo si quieres.")
                        return

            # Descargar la imagen en local
        

        response = openai.Image.create_variation(
            image=open('imgs/modify.png', "rb"),        
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await ctx.send(image_url)
    except:
        await ctx.send(content="Recuerda cumplir las siguientes reglas para poder procesar tu imagen:\n1.- La imagen deber ser .png\n2.- La imagen debe pesar menos de 4 MB\n3.- La imagen debe ser cuadrada, por ejemplo 500x500, 700x700, etc.")




bot.run(TOKEN)
