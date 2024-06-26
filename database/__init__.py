""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""


import aiosqlite
import random
from utils.classes import Champion, Champions


class DatabaseManager:
    def __init__(self, *, connection: aiosqlite.Connection) -> None:
        self.connection = connection

    async def add_warn(
        self, user_id: int, server_id: int, moderator_id: int, reason: str
    ) -> int:
        """
        This function will add a warn to the database.

        :param user_id: The ID of the user that should be warned.
        :param reason: The reason why the user should be warned.
        """
        rows = await self.connection.execute(
            "SELECT id FROM warns WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            warn_id = result[0] + 1 if result is not None else 1
            await self.connection.execute(
                "INSERT INTO warns(id, user_id, server_id, moderator_id, reason) VALUES (?, ?, ?, ?, ?)",
                (
                    warn_id,
                    user_id,
                    server_id,
                    moderator_id,
                    reason,
                ),
            )
            await self.connection.commit()
            return warn_id

    async def remove_warn(self, warn_id: int, user_id: int, server_id: int) -> int:
        """
        This function will remove a warn from the database.

        :param warn_id: The ID of the warn.
        :param user_id: The ID of the user that was warned.
        :param server_id: The ID of the server where the user has been warned
        """
        await self.connection.execute(
            "DELETE FROM warns WHERE id=? AND user_id=? AND server_id=?",
            (
                warn_id,
                user_id,
                server_id,
            ),
        )
        await self.connection.commit()
        rows = await self.connection.execute(
            "SELECT COUNT(*) FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None else 0

    async def get_warnings(self, user_id: int, server_id: int) -> list:
        """
        This function will get all the warnings of a user.

        :param user_id: The ID of the user that should be checked.
        :param server_id: The ID of the server that should be checked.
        :return: A list of all the warnings of the user.
        """
        rows = await self.connection.execute(
            "SELECT user_id, server_id, moderator_id, reason, strftime('%s', created_at), id FROM warns WHERE user_id=? AND server_id=?",
            (
                user_id,
                server_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list


    async def add_player(
        self, discord_id: int
    ) -> None:
        """
        This function will add a player to the database.

        :param discord_id: The ID of the player that should be added.
        """
        await self.connection.execute(
            "INSERT INTO players(discord_id) VALUES (?)",
            (
                discord_id,
            ),
        )
        await self.connection.commit()


    async def get_player(
        self, discord_id: int
    ) -> dict:
        """
        This function will get a player from the database.

        :param discord_id: The ID of the player that should be retrieved.
        :return: The player from the database.
        """
        rows = await self.connection.execute(
            "SELECT * FROM players WHERE discord_id=?",
            (
                discord_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result
        
    
    async def get_players(
        self,
    ) -> list:
        """
        This function will get all players from the database.

        :return: A list of all players from the database.
        """
        rows = await self.connection.execute(
            "SELECT * FROM players",
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row)
            return result_list


    async def remove_player(
        self, discord_id: int
    ) -> None:
        """
        This function will remove a player from the database.

        :param discord_id: The ID of the player that should be removed.
        """
        await self.connection.execute(
            "DELETE FROM players WHERE discord_id=?",
            (
                discord_id,
            ),
        )
        await self.connection.commit()


    async def add_game(
        self, random_champion: bool, impostor_mode: bool) -> int:
        """
        This function will add a game to the database.

        :param random_champion: The random champion mode.
        :param impostor_mode: The impostor mode.
        """
        rows = await self.connection.execute(
            "SELECT id FROM games ORDER BY id DESC LIMIT 1",
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            game_id = result[0] + 1 if result is not None else 1

        await self.connection.execute(
            "INSERT INTO games(id, random_champion, impostor_mode) VALUES (?, ?, ?)",
            (
                game_id,
                random_champion,
                impostor_mode,
            ),
        )
        await self.connection.commit()

        return game_id

    
    async def add_player_to_game(
        self, game_id: int, player_id: int
    ) -> None:
        """
        This function will add a player to a game in the database.

        :param game_id: The ID of the game where the player should be added.
        :param player_id: The ID of the player that should be added.
        """

        lane = random.choice(["top", "jungle", "mid", "bot", "support"])
        champion = Champions().get_random_champion_name(lane)

        await self.connection.execute(
            "INSERT INTO role_assignments(player_id, game_id, lane, champion) VALUES (?, ?, ?, ?)",
            (
                player_id,
                game_id,
                lane,
                champion,
            ),
        )
        await self.connection.commit()

    
    async def add_role_assignment(
        self, player_id: int, game_id: int, lane: str, champion: str
    ) -> None:
        """
        This function will add a role assignment to the database.

        :param player_id: The ID of the player that should be assigned.
        :param game_id: The ID of the game where the player should be assigned.
        :param lane: The lane of the player.
        :param champion: The champion of the player.
        """

        await self.connection.execute(
            "INSERT INTO role_assignments(player_id, game_id, lane, champion) VALUES (?, ?, ?, ?)",
            (
                player_id,
                game_id,
                lane,
                champion,
            ),
        )
        await self.connection.commit()


    async def update_role_assignment(
        self, player_id: int, game_id: int, lane: str, champion: str
    ) -> None:
        """
        This function will update a role assignment in the database.

        :param player_id: The ID of the player that should be updated.
        :param game_id: The ID of the game where the player should be updated.
        :param lane: The lane of the player.
        :param champion: The champion of the player.
        """

        await self.connection.execute(
            "UPDATE role_assignments SET lane=?, champion=? WHERE player_id=? AND game_id=?",
            (
                lane,
                champion,
                player_id,
                game_id,
            ),
        )
        await self.connection.commit()

    
    async def get_role_assignment(
        self, player_id: int, game_id: int
    ) -> dict:
        """
        This function will get a role assignment from the database.

        :param player_id: The ID of the player that should be retrieved.
        :param game_id: The ID of the game where the player should be retrieved.
        :return: The role assignment from the database.
        """
        rows = await self.connection.execute(
            "SELECT * FROM role_assignments WHERE player_id=? AND game_id=?",
            (
                player_id,
                game_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchone()
            return result

    
    async def get_connected_players(
        self, game_id: int
    ) -> list:
        """
        This function will get all connected players from the database.

        :param game_id: The ID of the game that should be checked.
        :return: A list of all connected players from the database.
        """
        rows = await self.connection.execute(
            "SELECT player_id, lane FROM role_assignments WHERE game_id=?",
            (
                game_id,
            ),
        )
        async with rows as cursor:
            result = await cursor.fetchall()
            result_list = []
            for row in result:
                result_list.append(row[0])
            return result_list

