import pygame
import random

pygame.mixer.init()

# Fish Caught Sound
sound_files = [
    "Octopus Get Sound.wav", "Narwhal Get Sound.wav", "Starfish 1 Get Sound.mp3",
    "Eel 1 Get Sound.mp3", "Dartfish 1 Get Sound.mp3", "Eel 2 Get Sound.mp3",
    "Dartfish 2 Get Sound.mp3", "Anglerfish Get Sound.mp3", "Bubblefish Get Sound.mp3"
]

fish_sounds = [pygame.mixer.Sound(s) for s in sound_files]

current_channel = None

pygame.mixer.music.load("3-19 Run, Jump, Throw! 1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Reel in fish sound effects
Calm_Catch_sound = pygame.mixer.Sound("Calm_Catch.wav")
Intense_Catch_sound = pygame.mixer.Sound("Intense_Catch.wav")


pygame.init()
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Fishing Madness")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

fish_difficulty = [10, 10, 10, 10, 5, 5, 5, 2.5, 2.5,]

# Fish Types
fish_names = [
    "Bubblefish (Common).jpg", "AnglerFish (Common).jpg", "Purple Dartfish (Common).jpg", "Marsh Eel (Common).jpg", "Tail Spiked Dartfish (Rare).jpg",
    "Midnight Eel (Rare).jpg", "Seafoam Magenta Starfish (Rare).jpg", "Narwhal ( Very Rare).jpg", "Speckled Great Octopus (Very Rare).jpg"    
]


fish_files = [
    f"Bubblefish (Common).jpg",
    "AnglerFish (Common).jpg",
    "Purple Dartfish (Common).jpg",
    "Marsh Eel (Common).jpg",
    "Tail Spiked Dartfish (Rare).jpg",
    "Midnight Eel (Rare).jpg",
    "Seafoam Magenta Starfish (Rare).jpg",
    "Narwhal ( Very Rare).jpg",
    "Speckled Great Octopus (Very Rare).jpg",

]

fish_images = [pygame.image.load(f).convert_alpha() for f in fish_files]


title_bg = pygame.image.load("Fishing Madness Background.jpg").convert()
title_bg = pygame.transform.scale(title_bg, (1200, 600))

game_bg = pygame.image.load("Second Fishing Background.png").convert()
game_bg = pygame.transform.scale(game_bg, (1200, 600))



fish_pool = list(range(10))
rarity_weights = [20, 20, 20, 20, 20, 5, 5, 5, 1, 1]

state = "Title Screen"

start_button_rect = pygame.Rect(500, 250, 200, 80)
pygame.mixer.music.load('Wii Sports Resort Title Screen.mp3')
pygame.mixer.music.play(-1)

inventory = {i: 0 for i in range(10)}
current_fish = None
show_timer = 0
reel_progress = 0
bite_timer = 0

running = True
while running:
    ticks = pygame.time.get_ticks()
    screen.blit(game_bg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and state == "Title Screen":
            if start_button_rect.collidepoint(event.pos):
                state = "Let's Fish"
                bite_timer = ticks + random.randint(2000, 5000)
                pygame.mixer.music.fadeout(1000)
                pygame.mixer.music.load("3-19 Run, Jump, Throw! 1.mp3")
                pygame.mixer.music.play(-1)
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state == "Waiting":
                state = "Let's Fish"
                bite_timer = ticks + random.randint(2000, 5000)
            
        if state == "Reel in":
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                reel_progress += fish_difficulty[current_fish]
                
                # sound effect for Calm_Catch and Intense_Catch
                if fish_difficulty[current_fish] >= 10:
                    if not pygame.mixer.get_busy():
                        Calm_Catch_sound.play()
                else:
                    if not pygame.mixer.get_busy():
                        Intense_Catch_sound.play()


    if state == "Let's Fish" and ticks >= bite_timer:
        state = "Fish on"
    
    if state == "Fish on":
        # Press Arrow key RIGHT to reel in
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            state = "Reel in"
            current_fish = random.choices(fish_pool, weights=rarity_weights)[0]
    
    if state == "Reel in" and reel_progress >= 100:
        state = "Fish Caught"
        show_timer = ticks + 5000 # Here it desplays the fish that was caught
        inventory[current_fish] += 1
        reel_progress = 0
        pygame.mixer.music.pause()
        current_channel = fish_sounds[current_fish].play()

    if current_channel: 
        if not current_channel.get_busy():
            pygame.mixer.music.unpause()
            current_channel = None 


    if state == "Fish Caught" and ticks >= show_timer:
        state = "Waiting"
        current_fish = None

    pygame.draw.rect(screen, (155, 48, 255, 255), (950, 0, 250, 700))
    title_surf = font.render("Fish Caught", True, (255, 255, 255))
    screen.blit(title_surf, (970, 20))

    y_offset = 80
    for fish_id, count in inventory.items():
        if count > 0:
            small_fish = pygame.transform.scale(fish_images[fish_id], (40, 40))
            screen.blit(small_fish, (965, y_offset))
            count_surf = font.render(f"x {count}", True, (255, 255, 255))
            screen.blit(count_surf, (1020, y_offset + 5))
            y_offset +=60
        
    if state == "Fish on":
        txt = font.render("FISH!", True, (255, 0, 0))
        screen.blit(txt, (450, 300))
    
    if state == "Reel in":
        pygame.draw.rect(screen, (0, 0, 0), (400, 350, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (400, 350, reel_progress * 2, 20))
        txt = font.render("Reel it in!", True, (255, 255, 255))
        screen.blit(txt, (420, 310))

    if state == "Fish Caught" and current_fish is not None:
        screen.blit(fish_images[current_fish], (400, 350))
        if state == "Fish Caught" and current_fish is not None:
            screen.blit(fish_images[current_fish], (400, 350))

            fish_name = fish_names[current_fish]
            total_caught = inventory[current_fish]

            name_surf = font.render(f"You caught a {fish_name}!", True, (255, 20, 147, 255))
            count_surf = font.render(f"Total {fish_name}s: {total_caught}", True, (255, 20, 147, 255))
    
            screen.blit(name_surf, (250, 70))
            screen.blit(count_surf, (200, 20))
            
    if state == "Title Screen":
        screen.blit(title_bg, (0, 0))
        
    
        title_font = pygame.font.SysFont("Arial", 80)
        title_surf = title_font.render("Fishing Madness", True, (255, 255, 255))
        screen.blit(title_surf, (350, 100))
        

        pygame.draw.rect(screen, (0, 178, 238, 255), start_button_rect)
        btn_font = pygame.font.SysFont("Arial", 40)
        btn_surf = btn_font.render("START", True, (255, 255, 255))
        screen.blit(btn_surf, (545, 265))          


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
