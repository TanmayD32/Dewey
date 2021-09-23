import discord 
from discord.ext import commands
client = commands.Bot(command_prefix='!')
token = 'Replace your Bot Token with this text' #Your bot token

# Some variables
bot1 = "`@` - Bot Prefix"

bot2 = "`aboutme` - To get information about me"
bot3 = "`purge` - To delete a message"
bot4 = "`kick` - To kick a dirty member from the server"
bot5 = "`ban` - To Ban a nerd from the server"
bot6 = "`unban` - To Unban a member from the server"
bot7 = "`mute` - To mute a trash talk member"
bot8 = "`unmute` - To unmute a member"
bot9 = "`avatar` - To show a member's profile picture"
bot10 = "`addpoll` To add a poll"
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Dewey")) #bot rich presense (watching)
    print("Dewey is Online on discord!") #Start event of the bot 

@client.command() #about bot (optional)
async def aboutme(ctx):
    await ctx.send(bot1)
    await ctx.send(bot2)
    await ctx.send(bot3)
    await ctx.send(bot4)
    await ctx.send(bot5)
    await ctx.send(bot6)
    await ctx.send(bot7)
    await ctx.send(bot8)
    await ctx.send(bot9)
    await ctx.send(bot10)
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
    await ctx.message.delete()

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await ctx.send(member.name+" Was Kicked from the server: "+reason)
    await member.kick(reason=reason)

@client.command(aliases=['b']) #ban a member
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "No reason provided"):
    await ctx.send(member.name + " Has been banned from the server: "+reason)
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
            await ctx.send(member_name +" Was Unbanned from this server!" )
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
@client.command(aliases=['user','info']) #This will give Info of A person.
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.name , description = member.mention , colour = discord.Colour.red())
    embed.add_field(name = "ID", value = member.id , inline = True)
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

#-------------------------------------------------------------------------------------------------------[Bot Token]--------------------------------------------------------------------------------------------------
client.run(token) # Bot token register
