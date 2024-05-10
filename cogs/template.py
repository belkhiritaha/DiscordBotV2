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
from utils.classes import Champion, Champions


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


class GameButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Join the game", style=discord.ButtonStyle.blurple)
    async def join(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        try:
            user_id = interaction.user.id
            self.value = user_id
            await interaction.response.send_message(f"Type `!get_champ <gameId>` to get your champion.", ephemeral=True)
        except Exception as e:
            print(e)
        self.stop()


class GetChampButtons(discord.ui.View):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

    @discord.ui.button(label="Top", style=discord.ButtonStyle.blurple)
    async def top(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "top"
        self.stop()

    @discord.ui.button(label="Jungle", style=discord.ButtonStyle.blurple)
    async def jungle(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "jungle"
        self.stop()

    @discord.ui.button(label="Mid", style=discord.ButtonStyle.blurple)
    async def mid(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "mid"
        self.stop()

    @discord.ui.button(label="ADC", style=discord.ButtonStyle.blurple)
    async def bot(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "bot"
        self.stop()

    @discord.ui.button(label="Support", style=discord.ButtonStyle.blurple)
    async def support(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ) -> None:
        self.value = "support"
        self.stop()



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
            description=f"**{result.name}** ({result.lane})\n\n{result.title}\n\n{result.description}\n\n[OP.GG Link](https://www.op.gg/champions/{result.name}/build/)",
            color=0xBEBEFE,
        )
        embed.set_thumbnail(url=result.icon)
        
        await message.edit(embed=embed, view=None, content=None)

    
    @commands.hybrid_command(
        name="register", description="Register a new player in the database."
    )
    async def register(self, context: Context) -> None:
        """
        This function will register a new player in the database.

        :param context: The hybrid command context.
        """
        await self.bot.database.add_player(str(context.author.id))
        await context.send("You have been registered in the database.")
        
        players = await self.bot.database.get_players()
        print(players)


    @commands.hybrid_command(
        name="add_game", description="Register a new game in the database.", pass_context=True
    )
    async def add_game(self, context: Context) -> None:
        """
        This function will register a new game in the database.

        :param context: The hybrid command context.
        """
        game_id = await self.bot.database.add_game(random_champion=True, impostor_mode=True)
        embed = discord.Embed(title="Among Us Game", description=f"Game ID: {game_id}\n\nClick on the button below to join the game.\n\nConnected players:\nNone...", color=0xBEBEFE)
        buttons = GameButtons()
        message = await context.send(embed=embed, view=buttons)

        max_players = 5

        while True:
            await buttons.wait()
            clicker_id = buttons.value

            await self.bot.database.add_player_to_game(game_id, clicker_id)
            connected_players = await self.bot.database.get_connected_players(game_id)
            connected_players_str = " ".join(["<@" + str(player) + ">" for player in connected_players])
            embed = discord.Embed(title="Among Us Game", description=f"Game ID: {game_id}\n\nClick on the button below to join the game.\n\nConnected players:\n{connected_players_str}", color=0xBEBEFE)
            buttons = GameButtons()
            await message.edit(embed=embed, view=buttons)
            
            # Check if the maximum number of players has been reached
            if len(connected_players) >= max_players:
                break

        # Optionally, you can perform additional actions after reaching the maximum number of players
        await context.send("Maximum number of players reached. The game is now full.")


    @commands.hybrid_command(
        name="get_champ", description="Get your champion for the game."
    )
    async def get_champ(self, context: Context, game_id: int) -> None:
        """
        This function will get the champion of the player for the game.

        :param context: The hybrid command context.
        :param game_id: The ID of the game where the player should get the champion.
        """
        player_id = context.author.id
        print(player_id, game_id)
        response = await self.bot.database.get_role_assignment(player_id, game_id) # (player_id, game_id, lane, champion)
        if response is None:
            await context.send("You are not registered in the game.")
        else:
            champ = Champions().get_champion_by_name(response[3])
            embed = discord.Embed(title="Among Us Game", description=f"Game ID: {game_id}\n\nPlayer: <@{player_id}>\n\nLane: {response[2]}\n\nChampion: {champ.name} ({champ.lane})\n\n{champ.title}\n\n{champ.description}\n\n[OP.GG Link](https://www.op.gg/champions/{champ.name}/build/)\n\nClick on one of the buttons below to switch lane / reroll your champion.", color=0xBEBEFE)
            embed.set_thumbnail(url=champ.icon)
            buttons = GetChampButtons()
            message = await context.send(embed=embed, view=buttons)
            await buttons.wait()
            lane = buttons.value
            champ = Champions().get_random_champion(lane)
            await self.bot.database.update_role_assignment(player_id, game_id, lane, champ.name)
            embed = discord.Embed(title="Among Us Game", description=f"Game ID: {game_id}\n\nPlayer: <@{player_id}>\n\nLane: {lane}\n\nChampion: {champ.name} ({champ.lane})\n\n{champ.title}\n\n{champ.description}\n\n[OP.GG Link](https://www.op.gg/champions/{champ.name}/build/)\n\nRerolls left: 1", color=0xBEBEFE)
            embed.set_thumbnail(url=champ.icon)
            buttons = GetChampButtons()
            await message.edit(embed=embed, view=buttons)
            await buttons.wait()
            lane = buttons.value
            champ = Champions().get_random_champion(lane)
            await self.bot.database.update_role_assignment(player_id, game_id, lane, champ.name)
            embed = discord.Embed(title="Among Us Game", description=f"Game ID: {game_id}\n\nPlayer: <@{player_id}>\n\nLane: {lane}\n\nChampion: {champ.name} ({champ.lane})\n\n{champ.title}\n\n{champ.description}\n\n[OP.GG Link](https://www.op.gg/champions/{champ.name}/build/)\n\nRerolls left: 0", color=0xBEBEFE)
            embed.set_thumbnail(url=champ.icon)
            await message.edit(embed=embed, view=None)

        


        
# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
async def setup(bot) -> None:
    await bot.add_cog(AmongUs(bot))
