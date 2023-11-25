# personality_manager.py
import json


class PersonalityManager:
    def __init__(self):
        with open('personalities.json', "r") as f:
            self.personalities_data = json.load(f)
