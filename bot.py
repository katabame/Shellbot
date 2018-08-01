# encoding: utf-8
import json
import discord
import os
import sys
import subprocess
import asyncio
from datetime import datetime

# load config file
with open('config.json', encoding='utf-8') as file:
    config = json.load(file)

def truncate(string, length, ellipsis='...'):
    return string[:length] + (ellipsis if string[length:] else '')

class Client(discord.Client):
    async def on_ready(self):
        print('[ OK ] Shellbot started')
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(f'<@{self.user.id}> ```'):
            command = message.content.replace(f'<@{self.user.id}>', '').strip().strip('```')

            print(f'[EXEC] @{message.author}: {command}')

            embed = discord.Embed(title='Run')
            embed.set_author(name='Shellbot', url='https://github.com/katabame/shellbot')
            try:
                response = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=1)
                embed.colour = discord.Colour.green()
                embed.add_field(name='StdOut', value=f'```{truncate(response.stdout.decode(), 1015)}```')
                embed.add_field(name='ExitCode', value=response.returncode, inline=True)
                embed.add_field(name='Status', value='Complete')
            except subprocess.CalledProcessError as response:
                embed.colour = discord.Colour.red()
                embed.add_field(name='StdOut', value=f'```{truncate(response.stderr.decode(), 1015)}```')
                embed.add_field(name='ExitCode', value=response.returncode, inline=True)
                embed.add_field(name='Status', value='Error')
            except subprocess.TimeoutExpired as response:
                embed.colour = discord.Colour.red()
                embed.add_field(name='StdOut', value=f'```{truncate(response.stderr.decode(), 1015)}```')
                embed.add_field(name='Status', value='Timeout')

            embed.timestamp = datetime.now()
            await message.channel.send(embed=embed)

if __name__ == '__main__':
    print('[LOAD] Starting Shellbot...')
    client = Client()
    client.run(config['token'])
