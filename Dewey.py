import discord 
from discord.ext import commands
from playsound import playsound # Use 'pip install playsound'
from colors import *

client = commands.Bot(command_prefix='?')
client.remove_command('help')
token = 'REPLACE YOUR BOT TOKEN WITH THIS TEXT' 

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@client.event
async def on_ready():
    print("Dewey is Online on discord!") #On ready Print
    playsound('path\\ding.mp3') # Paste the music path which you want to use it. eg- C:\\Users\Tanmay\\Desktop\\dewey\\dewey\\main\\ding.mp3. Also don't forgot to use \\ in the path, otherwise it will won't work
	#You can use my 'ding.mp3' file for startup sound. Provided in the folder

@client.command()
async def setstatus(ctx,*,status='Dewey'):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{status}")) #To set custom Status for your bot by discord command.
    await ctx.send(f'Bot Status Was Changed To: **{status}**')
    await ctx.message.delete()

@client.group(invoke_without_command=True) # about dewey. 
async def help(ctx):
        embedVar = discord.Embed(title="About Dewey", description=" ", color=0x00ff00)
        embedVar.add_field(name=" Dewey is a Discord Bot Which Can Moderate Your Server.", value= 'Bot Code Is Available On: **https://github.com/TanmayD32/Dewey**', inline=False)
        embedVar.add_field(name="Prefix", value="?", inline=False)
        embedVar.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/915937970987618334/915947540887781376/346ec84c3d4c1c196e121e1662800e10_1.png')
        embedVar.add_field(name="help", value="To get information about Dewey", inline=False)
        embedVar.add_field(name="purge", value="To delete messages", inline=False)
        embedVar.add_field(name="kick", value="To kick a person", inline=False)
        embedVar.add_field(name="ban", value="To Ban a person", inline=False)
        embedVar.add_field(name="mute", value="To mute a person", inline=False)
        embedVar.add_field(name="unmute", value="To Unmute a person", inline=False)
        embedVar.add_field(name="avatar", value="To see avatar of guild member", inline=False)
        embedVar.add_field(name="addpoll", value="To Add new Pool", inline=False)
        embedVar.add_field(name="whois", value="To get Information about a member", inline=False)
        embedVar.add_field(name="say", value="To Say somthing", inline=False)
        embedVar.add_field(name="create_channel", value="To Create a Channel", inline=False)
        embedVar.add_field(name="create_role", value="To Create a Role", inline=False)
        embedVar.add_field(name="setstatus", value="To Set Bot Status On Discord", inline=False)
        embedVar.add_field(name="announce", value="To Announce A Message", inline=False)
        embedVar.add_field(name="s", value="To Give Suggestion", inline=False)
        embedVar.set_footer(text='Made By Tanmay. Github: https://github.com/TanmayD32')
        await ctx.send(embed=embedVar)

        embed = discord.Embed(title = 'Useful links', color=0x00ff00)  # Useful links
        embed.description = '''[Official Github](https://github.com/TanmayD32/Dewey)
                            [Bot Code](https://github.com/TanmayD32/)'''
        await ctx.send(embed=embed)
        await ctx.message.delete()
    

#---------------------------------------------------------------------------------------------------[mod commands]------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['cls','purge']) #purge 
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2,):
    limit1 = 0
    error_embed = discord.Embed(title = f':x: Unable to purge {amount} Messages', description=f'Too many messages to purge at a same time. Or the message are older than 14 days Which cannot be purged.', color= colors.red)
    embedVar = discord.Embed(title = f':white_check_mark: Messages Purged', description=f'**{amount}** Messages Was Purged By User `{ctx.author}`', color=0x00ff00)
    if amount >= 15:
        await ctx.channel.purge(limit = limit1)
        await ctx.send(embed=error_embed)
        await ctx.message.delete()
    else:
        await ctx.channel.purge(limit = amount+1)
        await ctx.send(embed=embedVar)

@client.command() # kick
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    embedVar = discord.Embed(title = f':no_entry: `{member.name}` was kicked. '+ reason)
    await ctx.send(embed=embedVar)
    # await ctx.send(member.name+" Was Kicked from the server: "+reason)
    await member.kick(reason=reason)

@client.command(aliases=['b']) #ban a member
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
    embedVar = discord.Embed(title=f":hammer: Ban Hammer has been spoken to `{member.name}` "+ reason, color=0x00ff00)
    await ctx.send(embed=embedVar)
    # await ctx.send(member.name + " Has been banned from the server: "+reason)
    await member.send("You have been banned from the server")
    await member.ban(reason=reason)
    await ctx.message.delete()

@client.command(aliases=['ub']) #Unban a member
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):

            await ctx.guild.unban(user)
            # await ctx.send(member_name +" Was Unbanned from this server!" )
            embedVar = discord.Embed(title= f":white_check_mark: {member_name} Was unbanned.", color=0x00ff00)
            await ctx.send(embed=embedVar)
            await ctx.message.delete()
            return
    await ctx.send(member+" Was not found!")
    await ctx.message.delete()

@client.command() # Mute command
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member:discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name='muted' or 'Muted' or 'mute' or 'Mute')
    guild = ctx.guild
    if muted_role not in guild.roles:
        perm = discord.permissions(send_messages=False)
        await guild.create_role('Muted', permissions=perm)
        await member.add_roles((muted_role))
        embed = discord.Embed(title = f':mute: ``{member}`` was muted', color=0x00ff00)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        await member.add_roles(muted_role)
        embed = discord.Embed(title = f':mute: ``{member}`` was muted', color=0x00ff00)
        await ctx.send(embed=embed)
        await ctx.message.delete()

@client.command() #unmute command
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member:discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name='muted' or 'Muted' or 'mute' or 'Mute')
    await member.remove_roles(muted_role)
    embed = discord.Embed(title = f':white_check_mark: ``{member}`` was Unmuted', color=0x00ff00)
    await ctx.send(embed=embed)  
    await ctx.message.delete() 

@client.command(aliases=['w']) #warn a person
@commands.has_permissions(kick_members = True)
async def warn(ctx,member : discord.Member,*,reason= "No reason provided"):
    embedVar = discord.Embed(title= f'``{member}`` Was Warned By ``{ctx.author}``', description = f'Reason: {reason}', color=0x00ff00)
    await ctx.send(embed=embedVar)
    await ctx.message.delete()
#-----------------------------------------------------------------------------------[Error Handleing]------------------------------------------------------------------------------------------------------
@client.event
async def on_command_error(ctx, error): 
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You Don't have Permission to do that! ;-;")
        embed = discord.Embed(title = f":no_entry: ``{ctx.author}`` Access Denied", color= colors.red)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    if isinstance(error,commands.MissingRequiredArgument): 
        await ctx.send("Please enter all the required arguments!")
        await ctx.message.delete()
#-----------------------------------------------------------------------------------[Embeds]---------------------------------------------------------------------------------------------------------------
@client.command(aliases=['user']) #User Info command
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
    guild = ctx.guild
    roles = [role for role in member.roles]
    embed = discord.Embed(title = member.name , description = member.mention , colour = member.color)
    embed.add_field(name = "ID", value = member.id , inline = False )
    embed.add_field(name = "Server Name", value= guild.name, inline = False)
    embed.add_field(name=f'Roles ({len(roles)})', value = " " .join([role.mention for role in roles]), inline = False)
    embed.add_field(name="Is BOT?", value=member.bot, inline = False)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(text = "Created by Dewey Bot")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command(aliases=['av']) #Can show the Profile picture of a perticular  user
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(
        colour = discord.Colour.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)
    await ctx.message.delete()

@client.command() # pool
@commands.has_permissions(kick_members = True)
async def addpoll(ctx,*, msg):
    channel = ctx.channel
    try:
        op1 , op2 = msg.split("or")
        txt = f''':one: **{op1}** 

                  :two: **{op2}**'''
    except:
        await channel.send("Correct Syntax: Choice1 or Choise2")
        return

    embed= discord.Embed(title=f"POLL", description = txt, color=0x00ff00)
    embed.set_footer(text = "Created by Dewey Bot")
    message_ = await channel.send(embed=embed)
    await message_.add_reaction("1️⃣")
    await message_.add_reaction("2️⃣")
    await ctx.message.delete()

@client.command(aliases=['role']) #create's a new role
@commands.has_permissions(manage_roles=True) 
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f'Role `{name}` has been created')

@client.command(aliases=['new_channel', 'channel']) #Create's a new channel
async def create_channel(ctx, *, name):
    guild = ctx.message.guild
    await guild.create_text_channel(f'{name}')
    await ctx.send(f'Channel `{name}` has been created')
    await ctx.message.delete()

@client.command() # Its fine
async def say (ctx, *, say):
    await ctx.send(f'{ctx.author.mention} Said: **{say}**')
    await ctx.message.delete()

@client.command() # You can embedded message
async def announce(ctx, *, msg):
    await ctx.send(f'{ctx.guild.default_role}')
    embedVar = discord.Embed(title=":warning: Announcement", description=f"**{msg}**", color=0x00ff00)  
    embedVar.set_footer(text=f'Announced By - {ctx.author}')
    await ctx.send(embed=embedVar)

@client.command(aliases=['s']) # Suggestion command
async def suggestion(ctx,*, message):
    await ctx.send(f'Your suggestion has been recorded: **{message}**')
    # await ctx.message.delete()
    channel = client.get_channel(890426648556621867) # channel ID which you want to recive member's suggestion
    embed = discord.Embed(title=f'''New suggestion recived from ``{ctx.author}`` 
Server: ``{ctx.guild}``''', description=f'{message}', color=0x00ff00)
    await channel.send(embed=embed)
    await ctx.message.delete()

@client.command() # To Send DM 
@commands.has_permissions(kick_members = True)
async def reply(ctx, member: discord.Member,*, msg):
    guild = ctx.guild
    channel = await member.create_dm()
    await channel.send(f'{member.mention}')
    embedVar = discord.Embed(title = f'You Got A Message From: ``{ctx.author}``', description = f'From Server: ``{guild}``', color=0x00ff00)
    embedVar.add_field(name = f'Message:', value=f'{msg}')
    await ctx.send(f'Message Was Sent to User **{member}**, Message: **{msg}**')
    await channel.send(embed=embedVar)
    await ctx.message.delete()

#-------------------------------------------------------------------------------------------------------[Bot Token]--------------------------------------------------------------------------------------------------
client.run(token) # Bot token register
