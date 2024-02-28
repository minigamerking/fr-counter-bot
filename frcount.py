import discord
import sqlite3
import mytokenforbot
import os
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)


@app.route('/')
def index():
    return '''<body style="margin: 0; padding: 0;">
    <iframe width="100%" height="100%" src="https://axocoder.vercel.app/" frameborder="0" allowfullscreen></iframe>
  </body>'''


def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()


keep_alive()
print("Server Running Because of Axo")
# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

conn = sqlite3.connect('fr_count.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS fr_count
             (guild_id INTEGER PRIMARY KEY, count INTEGER)''')
conn.commit()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

fr_count = 8


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global fr_count
    if message.author == client.user:
        return
    if 'fr' in message.content.lower():
        c.execute(
            'UPDATE fr_count SET count = count + 1 WHERE guild_id = ?', (message.guild.id,))
        conn.commit()

    if message.content.startswith('$counter'):
        c.execute('SELECT count FROM fr_count WHERE guild_id = ?',
                  (message.guild.id,))
        count = c.fetchone()[0]
        await message.channel.send(f'Amount of FRs: {count}')


try:
    token = mytokenforbot.token()
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
conn.close()
