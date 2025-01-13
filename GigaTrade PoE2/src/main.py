import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import datetime
import pygame
import configparser
import pydirectinput as pydi
import pywinauto
from discord_webhook import DiscordEmbed, DiscordWebhook

os.system('title GigaTrade PoE2')
game_window = "Path of Exile 2"
app = pywinauto.Application().connect(title = game_window)
window = app.window(title = game_window)
config = configparser.ConfigParser()
config.read('settings.ini')

# Discord settings =======================================================
use_discord = config.getboolean('Discord', 'use_discord')
webhook_url = config.get('Discord','webhook_url')
thumbnail_img = 'https://i.imgur.com/YAlAmHL.png' # Thumbnail image used in webhook
webhook = DiscordWebhook(url=webhook_url)

# Push notification settings (Currently Not Working) ======================
use_push = config.getboolean('Push', 'use_push')

#
file_path = config.get('PoE2', 'logfile_path') # Replace with path to your log file name
path = os.path.dirname(os.path.realpath(__file__))
sale_string = "I would like to buy"

pygame.mixer.init()
pygame.mixer.music.load(f"{path}\\Sounds\\SaleAlert.mp3") # Sale alert sound

# WIP, sending reply messages is currently not implimented
def send_reply(reply):
    pydi.keyDown('ctrl')
    pydi.press('enter')
    pydi.keyUp('ctrl')
    pydi.typewrite(reply)
    pydi.press('enter')

def timestamp_msg(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {message}"

def read_log(filename):
    print("Trade notifications enabled, do not close this window")
    print("Listening for new messages...\n")
    with open(filename, 'r', encoding="utf8") as file:
        file.seek(0, 2)
        while True:

            embed = DiscordEmbed(
                title='New trade request!',
                color="5CDBF0"
                )

            embed.set_thumbnail(url=thumbnail_img)

            line = file.readline()
            if line:
                result = line.split("@From ")
                if len(result) > 1:
                    if sale_string in line:    
                        embed.add_embed_field(name='Message', value=result[1])
                        embed.set_timestamp()
                        if use_discord:
                            try:
                                webhook.add_embed(embed)
                                response = webhook.execute(remove_embeds=True)
                                window.set_focus()
                            except:
                                print(response)

                        pygame.mixer.music.play()
                
                    print(timestamp_msg(result[1]), end='')
                    time.sleep(0.1)

if __name__ == "__main__":
    read_log(file_path)