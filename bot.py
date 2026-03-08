import json
import os
import threading

import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask

from discord_id_lookup import lookup_discord_id

# Carrega o token do bot de uma variável de ambiente para segurança
TOKEN = os.getenv('DISCORD_TOKEN')

# Define os intents necessários para o bot
intents = discord.Intents.default()
intents.message_content = True  # Permite ao bot ler o conteúdo das mensagens
intents.members = True          # Permite ao bot acessar informações de membros do servidor
intents.presences = True        # Permite ao bot acessar informações de presença

# Cria uma instância do bot com um prefixo de comando e os intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Pequeno servidor HTTP para manter uma porta aberta no Render (Web Service)
app = Flask(__name__)


@app.get('/')
def healthcheck():
    return 'Bot is running', 200


def run_web_server():
    port = int(os.getenv('PORT', '10000'))
    app.run(host='0.0.0.0', port=port)


@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    print(f'ID do Bot: {bot.user.id}')
    print('------')
    try:
        synced = await bot.tree.sync()
        print(f'Sincronizei {len(synced)} comandos de barra.')
    except Exception as e:
        print(f'Erro ao sincronizar comandos de barra: {e}')


@bot.command(name='ola')
async def hello(ctx):
    await ctx.send(f'Olá, {ctx.author.name}!')


@bot.command(name='info')
async def info(ctx):
    await ctx.send('Eu sou um bot de teste criado com discord.py!')


@bot.tree.command(name='id', description='Consulta informações de um ID do Discord.')
@app_commands.describe(user_id='O ID do usuário do Discord para consultar.')
async def id_command(interaction: discord.Interaction, user_id: str):
    await interaction.response.defer(ephemeral=True)  # Deferir a resposta para evitar timeout

    if not TOKEN:
        await interaction.followup.send("Erro: O token do bot não está configurado. Por favor, defina a variável de ambiente 'DISCORD_TOKEN'.")
        return

    # Chama a função de consulta
    result = await lookup_discord_id(user_id, TOKEN)

    if 'error' in result:
        await interaction.followup.send(f"Ocorreu um erro ao consultar o ID: {result['error']}")
    else:
        # Formata a resposta para o Discord
        response_message = """
