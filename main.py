import pygame
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VEL = 5
FONT = pygame.font.SysFont("comicsans", 30)
L_FONT = pygame.font.SysFont("comicsans", 50) # Suurempi fontti loppuruutuun
STAR_WIDTH, STAR_HEIGHT = 10, 20
STAR_VEL = 3

def draw(player, elapsed_time, stars):
    WINDOW.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {int(elapsed_time)}s", 1, ("white"))
    WINDOW.blit(time_text, (10, 10))

    pygame.draw.rect(WINDOW, (255, 0, 0), player)

    for star in stars:
        pygame.draw.rect(WINDOW, "white", star)

    pygame.display.update()

def main():
    run = True
    while run: # UUSI: Ulompi silmukka mahdollistaa uudelleenaloituksen
        player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0

        star_add_increment = 2000  # milliseconds
        star_count = 0
        stars = []
        hit = False
        playing = True

        while playing: # Varsinainen pelisilmukka
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            if star_count >= star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return # Sulkee ohjelman

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
                player.x += PLAYER_VEL

            for star in stars[:]:
                star.y += STAR_VEL
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    hit = True
                    playing = False # Poistuu pelisilmukasta
                    break

            if not hit:
                draw(player, elapsed_time, stars)

        # --- LOPETUSRUUTU ---
        if hit:
            waiting = True
            while waiting:
                WINDOW.fill("black") # Tai blittaa BG
                
                lost_text = L_FONT.render("YOU LOST!", 1, "red")
                score_text = FONT.render(f"Survival Time: {int(elapsed_time)}s", 1, "white")
                retry_text = FONT.render("Press 'R' to Restart or 'ESC' to Quit", 1, "yellow")
                
                WINDOW.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - 100))
                WINDOW.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2))
                WINDOW.blit(retry_text, (WIDTH/2 - retry_text.get_width()/2, HEIGHT/2 + 100))
                
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r: # Uusi peli
                            waiting = False
                        if event.key == pygame.K_ESCAPE: # Sulje peli
                            pygame.quit()
                            return


    pygame.quit()

if __name__ == "__main__":
    main()