import discord
import sqlite3
import mytokenforbot
import os
from flask import Flask
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

# Connect to the SQLite database
conn = sqlite3.connect('fr_count.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS fr_count
             (guild_id INTEGER PRIMARY KEY, count INTEGER)''')
conn.commit()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global fr_count
    if message.author == client.user:
        return
    if 'fr' in message.content.lower():
        # Update the count in the database
        c.execute(
            'INSERT OR IGNORE INTO fr_count (guild_id, count) VALUES (?, 0)', (message.guild.id,))
        c.execute(
            'UPDATE fr_count SET count = count + 1 WHERE guild_id = ?', (message.guild.id,))
        conn.commit()

    if message.content.startswith('$counter'):
        # Retrieve the count from the database
        c.execute('SELECT count FROM fr_count WHERE guild_id = ?',
                  (message.guild.id,))
        result = c.fetchone()
        if result:
            count = result[0]
            await message.channel.send(f'Amount of FRs: {count}')
        else:
            await message.channel.send("No FR messages found.")

try:
    token = mytokenforbot.token()
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print("Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e

conn.close()
