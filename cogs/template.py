""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import discord
import random
import json
from discord.ext import commands
from discord.ext.commands import Context


class Roles(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Top", style=discord.ButtonStyle.blurple)
    async def top_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "top"
        self.stop()

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.blurple)
    async def jungle_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "jungle"
        self.stop()

    @discord.ui.button(label="Mid", style=discord.ButtonStyle.blurple)
    async def mid_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "mid"
        self.stop()

    @discord.ui.button(label="ADC", style=discord.ButtonStyle.blurple)
    async def adc_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "bot"
        self.stop()

    @discord.ui.button(label="Support", style=discord.ButtonStyle.blurple)
    async def support_button(
        self, button: discord.ui.Button, interaction: discord.Interaction
    ) -> None:
        self.value = "support"
        self.stop()


class Champion:
    def __init__(self, name: str, lane: str, id: int, icon: str, title: str, description: str) -> None:
        self.name = name
        self.lane = lane
        self.id = id
        self.icon = icon
        self.title = title
        self.description = description

    def __str__(self) -> str:
        return f"{self.name} ({self.lane})"


# Class to read data from database/champions.json
class Champions:
    def __init__(self) -> None:
        with open("database/champions.json", "r") as file:
            self.champions = json.load(file)

    def get_random_champion(self, lane: str = None) -> Champion:
        if lane is None:
            lane = random.choice(["top", "jungle", "mid", "bot", "support"])
        champion = random.choice([champion for champion in self.champions if champion["lane"] == lane])
        return Champion(
            name=champion["name"],
            lane=lane,
            id=champion["id"],
            icon=champion["icon"],
            title=champion["title"],
            description=champion["description"],
        )



# Here we name the cog and create a new class for the cog.
class AmongUs(commands.Cog, name="amongus"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        name="random-champ", description="Get a random champion from League of Legends."
    )
    async def randomchamp(self, context: Context) -> None:
        """
        This function will get a random champion from League of Legends depending on the user's role.

        :param context: The hybrid command context.
        """
        buttons = Roles()
        embed = discord.Embed(description="What is your lane?", color=0xBEBEFE)
        message = await context.send(embed=embed, view=buttons)
        await buttons.wait()
        result = Champions().get_random_champion(buttons.value)
        embed = discord.Embed(
            description=f"**{result.name}** ({result.lane})\n\n{result.title}\n\n{result.description}",
            color=0xBEBEFE,
        )
        embed.set_thumbnail(url=result.icon)
        await message.edit(embed=embed, view=None, content=None)



# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(AmongUs(bot))
