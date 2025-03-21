from discord.ui import View, button
from discord import Button, ButtonStyle, Interaction
from CupidV3Database.matchingdb import Profile, MATCHING
from discord.ext.commands import Bot

class SubmissionView(View):
    def __init__(self, bot:Bot):
        self.bot = bot
        super().__init__(timeout=None)
    
    @button(label="Approve", style=ButtonStyle.green, custom_id='approve_button')
    async def approve_button(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        record = await MATCHING.find_one({"message_id":interaction.message.id})
        profile = Profile(record)
        await profile.update({"$set":{'approved':True}})
        self.children[1].disabled = True
        button.disabled = True
        profile_embed = profile.create_embed()
        profile_embed.color = 0x77DD77
        profile_embed.add_field(value=f'Approved by: {interaction.user.mention}', name='Approved')
        await interaction.message.edit(embed=profile_embed, view=self)
        await interaction.followup.send("Approved!", ephemeral=True)

        try:
            user = self.bot.get_user(profile.user_id)
            await user.send(f"Your profile was Approved! Swiping will come very soon! be excited for it :)\n[THANK YOU FOR YOUR PAITENCE SORRY THE BOT WAS BUGGING FOR A BIT]")
        except: 
            await interaction.followup.send(f"I couldnt dm {user.mention}!")

        match (profile.gender):
            case 'Male':
                channel = self.bot.get_channel(1307474580008599663)
            case 'Female':
                channel = self.bot.get_channel(1307474598060883968)
            case _:
                channel = self.bot.get_channel(1307480874119462952)
        
        profile_embed.color = 0xFFA1DC
        posted_msg = await channel.send(embed=profile_embed)
        profile.update({"$set":{'posted_channel':posted_msg.channel.id,'posted_message':posted_msg.id}})
    
    @button(label="Deny", style=ButtonStyle.red, custom_id='deny_button')
    async def deny_button(self, interaction:Interaction, button:Button):
        await interaction.response.defer()
        record = await MATCHING.find_one({"message_id":interaction.message.id})
        profile = Profile(record)
        await profile.update({"$set":{'approved':False}})
        self.children[0].disabled = True
        button.disabled = True
        profile_embed = profile.create_embed()
        profile_embed.color = 0xFF6961
        profile_embed.add_field(value=f'Denied by: {interaction.user.mention}', name='Denied')
        await interaction.message.edit(embed=profile_embed, view=self)
        await interaction.followup.send("Denied!", ephemeral=True)
        try:
            user = self.bot.get_user(profile.user_id)
            await user.send(f"Your profile was denied! Please edit it and resubmit it, denials happen usually because your bio isnt detailed, feel free to ask staff why")
        except: 
            await interaction.followup.send(f"I couldnt dm {user.mention}!")
        
