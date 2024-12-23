if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time

class GameState:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.active_bullets = []
            cls._instance.game_entities = []
            cls._instance.cancer_points = 0
            cls._instance.active_effects = {}  # Store active effects and their timers
        return cls._instance
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_bullet(self, bullet):
        self.active_bullets.append(bullet)
        
    def add_entity(self, entity):
        self.game_entities.append(entity)
        
    def remove_entity(self, entity):
        if entity in self.game_entities:
            self.game_entities.remove(entity) 
    
    def add_cancer(self, amount):
        self.cancer_points += amount
        if self.cancer_points >= 100:
            print("Too much cancer!") # We can expand this later
    
    def add_effect(self, effect_name, duration, player):
        self.active_effects[effect_name] = {
            'duration': duration,
            'start_time': time.time(),
            'player': player
        }
    
    def update_effects(self):
        current_time = time.time()
        effects_to_remove = []
        
        for effect_name, effect_data in self.active_effects.items():
            if current_time - effect_data['start_time'] > effect_data['duration']:
                if effect_name == "crack_speed":
                    effect_data['player'].speed /= 1.2
                effects_to_remove.append(effect_name)
        
        for effect in effects_to_remove:
            del self.active_effects[effect]