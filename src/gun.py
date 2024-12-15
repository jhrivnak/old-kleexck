import pygame, random

no_ammo_sound = None
gun_sounds = []
reload_sounds = []

def load_sounds():
    global no_ammo_sound, gun_sounds, reload_sounds
    no_ammo_sound = pygame.mixer.Sound("assets/audio/effects/gun/noAmmo.ogg")
    gun_sounds.clear()
    for i in range(1,7):
        gun_sounds.append(pygame.mixer.Sound(f"assets/audio/effects/gun/gunshot{i}.ogg"))
    reload_sounds.clear()
    for i in range(1,7):
        reload_sounds.append(pygame.mixer.Sound(f"assets/audio/effects/gun/reload{i}.ogg"))

def set_volume(vol):
    no_ammo_sound.set_volume(vol)
    for s in gun_sounds:
        s.set_volume(vol)
    for s in reload_sounds:
        s.set_volume(vol)

def play_no_ammo():
    no_ammo_sound.play()

def play_gunshot():
    random.choice(gun_sounds).play()

def play_reload_sound(idx):
    reload_sounds[idx].play()

def reload_gun(inventory_ammo, magazine_size, current_magazine, sound_muted, reload_duration, set_ammo_func):
    needed = magazine_size - current_magazine
    if needed <=0:
        return None
    if inventory_ammo < needed:
        needed = inventory_ammo
    if needed <= 0:
        return None
    # Return how many bullets we will add after reload completes
    return needed
