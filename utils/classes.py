import json
import random

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

    def get_random_champion_name(self, lane: str = None) -> str:
        if lane is None:
            lane = random.choice(["top", "jungle", "mid", "bot", "support"])
        champion = random.choice([champion for champion in self.champions if champion["lane"] == lane])
        return champion["name"]

    def get_champion_by_name(self, name: str) -> Champion:
        champion = next((champion for champion in self.champions if champion["name"] == name), None)
        if champion is None:
            return None
        return Champion(
            name=champion["name"],
            lane=champion["lane"],
            id=champion["id"],
            icon=champion["icon"],
            title=champion["title"],
            description=champion["description"],
        )