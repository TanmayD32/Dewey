import discord 
from discord.ext import commands
client = commands.Bot(command_prefix='!')
token = 'Replace your Bot Token with this text' #Your bot token

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.command() # You can now set status of the bot from discord. # New update- 1.2
async def setstatus(ctx,*, msg=' '):
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f'{msg}')) 

@client.event
async def on_ready():
#     await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Dewey")) #bot rich presense (watching)
    print("Dewey is Online on discord!") #Start event of the bot 

@client.command() # about dewey. (You can remove this event, and can add into a command {@client.command})
async def aboutme(ctx):
        embedVar = discord.Embed(title="Dewey Commands", description=" ", color=0x00ff00)
        embedVar.add_field(name="aboutme", value="To get information about me", inline=False)
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
        await ctx.send(embed=embedVar)
        await ctx.message.delete()

@client.command()
async def prefix(ctx):
    await ctx.send("`!`")


# @client.event() 
# async def on_member_join(member):
#     print(f'{member} Just joinded the server')

# @client.event() # the leave log. (console)
# async def on_member_remove(member):
#     print(f'{member} Just left the server')
#---------------------------------------------------------------------------------------------------[mod commands]------------------------------------------------------------------------------------------------------------------------------
@client.command(aliases=['cls','purge']) #purge 
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)
    await ctx.send(f'**{amount}** messages has been deleted')
    await ctx.message.delete()

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    embedVar = discord.Embed(title = f':no_entry: `{member.name}` was kicked. '+ reason)
    await ctx.send(embed=embedVar)
    # await ctx.send(member.name+" Was Kicked from the server: "+reason)
    await member.kick(reason=reason

@client.command(aliases=['b']) #ban a member
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
    embedVar = discord.Embed(title=f":hammer: Ban Hammer has been spoken to `{member.name}` "+ reason)
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
            embedVar = discord.Embed(title= f":white_check_mark: {member_name} Was unbanned.")
            await ctx.send(embed=embedVar)
            await ctx.message.delete()
            return
    await ctx.send(member+" Was not found!")
    await ctx.message.delete()


@client.command(aliases=['m']) #mute a person
@commands.has_permissions(kick_members = True)
async def mute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role() #put your role's ID here (Should not be having Permission of Send message in specific channel)

    await member.add_roles(muted_role)

    await ctx.send(member.mention +" Has been muted!")
    await ctx.message.delete()

@client.command(aliases=['unm']) #unmute a person
@commands.has_permissions(kick_members = True)
async def unmute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role() #put your role's ID here (Should not be having Permission of Send message in specific channel)

    await member.remove_roles(muted_role)

    await ctx.send(member.mention +" Has been unmuted!")
    await ctx.message.delete()

@client.command(aliases=['w']) #warn a person
@commands.has_permissions(kick_members = True)
async def warn(ctx,member : discord.Member,*,reason= "No reason provided"):
    await ctx.send(member.mention +" You Have been warned for a reason: "+reason)
    await ctx.message.delete()
#-----------------------------------------------------------------------------------[Error Handleing]------------------------------------------------------------------------------------------------------
@client.event
async def on_command_error(ctx,error): #this will print when a person types a mod command but he don't have permi.
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You Don't have Permission to do that! ;-;")
        await ctx.message.delete()
    if isinstance(error,commands.MissingRequiredArgument): #this will print when you will don't type all args in your command.
        await ctx.send("Please enter all the required arguments!")
        await ctx.message.delete()
#-----------------------------------------------------------------------------------[Embeds]---------------------------------------------------------------------------------------------------------------
@client.command(aliases=['user','info']) #This will give Info of A person. (Updated 1.0)
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
    roles = [role for role in member.roles]
    embed = discord.Embed(title = member.name , description = member.mention , colour = member.color)
    embed.add_field(name = "ID", value = member.id , inline = False )
    embed.add_field(name = "Server Name", value= member.display_name, inline = False)
    embed.add_field(name=f'Roles ({len(roles)})', value = " " .join([role.mention for role in roles]), inline = False)
    embed.add_field(name="Is BOT?", value=member.bot, inline = False)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(text = "Created by Dewey Bot")
    await ctx.send(embed=embed)
    await ctx.message.delete()

@client.command(aliases=['av']) #this will show you the avatar of the members.
async def avatar(ctx, member: discord.Member):
    show_avatar = discord.Embed(

        colour = discord.Colour.dark_blue()
    )
    show_avatar.set_image(url='{}'.format(member.avatar_url))
    await ctx.send(embed=show_avatar)
    await ctx.message.delete()
#------------------------------------------------------[Pool]-----------------------------------------------------------------------------------------------------------
@client.command()
#@commands.has_permissions(kick_members = True)
async def addpoll(ctx,*, msg):
    channel = ctx.channel
    try:
        op1 , op2 = msg.split("or")
        txt = f"React with ✅ for {op1} and ❎ for {op2}"
    except:
        await channel.send("Correct Syntax: Choice1 or Choise2")
        return

    embed= discord.Embed(title="Today's Poll!", description = txt,colour = discord.Colour.red())
    embed.set_footer(text = "Created by Dewey Bot")
    message_ = await channel.send(embed=embed)
    await message_.add_reaction("✅")
    await message_.add_reaction("❎")
    await ctx.message.delete()
#------------------------------------------------------------------------------------------------[New update- 1.0]------------------------------------------------------------------------------------------------------------------------------------

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
    await ctx.send(f'channel `{name}` has been created')
    await ctx.message.delete()

@client.command()
async def say (ctx, *, say):
    await ctx.send(f'{ctx.author.mention} `Said:` **{say}**')
    await ctx.message.delete()
		      
#------------------------------------------------------------------------------------------------[New update- 1.1]------------------------------------------------------------------------------------------------------------------------------------
	   
@client.command()
async def announce(ctx, *, ers):
    await ctx.send(f'{ctx.guild.default_role}')
    embedVar = discord.Embed(title=":warning: Announcement", description=f"**{ers}**", color=0x00ff00)
    # embedVar.add_field(name=f"{ers}", value=None, inline=False)
    embedVar.set_footer(text=f'Announced By - {ctx.author}')
    await ctx.send(embed=embedVar)
    await ctx.message.delete()
		      
#------------------------------------------------------------------------------------------------[New update- 1.2]------------------------------------------------------------------------------------------------------------------------------------
		      
@client.command() # Announcement command
async def announce(ctx, *, ers):
    await ctx.send(f'{ctx.guild.default_role}')
    embedVar = discord.Embed(title=":warning: Announcement", description=f"**{ers}**", color=0x00ff00)
    # embedVar.add_field(name=f"{ers}", value=None, inline=False)
    embedVar.set_footer(text=f'Announced By - {ctx.author}')
    await ctx.send(embed=embedVar)
    await ctx.message.delete()

@client.command(aliases=['suggestion']) # Suggestion command
async def s(ctx,*, message):
    await ctx.send(f'Your suggestion has been recorded: **{message}**')
    channel = client.get_channel(890426648556621867) # channel ID which you want to recive member's suggestion
    embed = discord.Embed(title=f'New suggestion recived from ``{ctx.author}``', description=f'**{message}**', color=0x00ff00)
    await channel.send(embed=embed)
#-------------------------------------------------------------------------------------------------------[Bot Token]--------------------------------------------------------------------------------------------------
client.run(token) # Bot token register
