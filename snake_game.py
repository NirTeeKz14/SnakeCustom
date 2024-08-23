import pygame
import random

pygame.init()
pygame.mixer.init()

# Chargement de la musique
try:
    pygame.mixer.music.load('Snake.io Music.mp3')
except pygame.error as e:
    print(f"Erreur de chargement de la musique: {e}")

haunted_music = 'Musique Angoissante Libre de Droit Gratuite qui Fait Peur Horreur _ Audionautix - Horror Music.mp3'

# Définition des couleurs
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
blink_color_1 = (100, 100, 100)
blink_color_2 = (0, 0, 0)

largeur_ecran = 800
hauteur_ecran = 600
taille_bloc = 20

fenetre_jeu = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption('Jeu Snake')

horloge = pygame.time.Clock()
police_score = pygame.font.SysFont("bahnschrift", 35)

haunted_mode = False
score_unlocked = 2

# Liste des messages effrayants
messages_effrayants = [
    "Je te vois...",
    "Tu ne devrais pas être dans ce mode",
    "N'essaie pas de quitter...",
    "Je suis derrière toi...",
    "C'est trop tard pour toi...",
    "Tu ne sortiras jamais...",
    "La fin est proche...",
    "Il est trop tard...",
    "Je suis toujours là...",
    "Regarde derrière toi...",
    "Tout est noir maintenant..."
]

dernier_message = None
temps_dernier_affichage = 0
intervalle_message = 5000
temps_min_avant_premier_message = 60000

def afficher_message(msg, couleur, position=None):
    mesg = police_score.render(msg, True, couleur)
    if position is None:
        position = [largeur_ecran / 6, hauteur_ecran / 3]
    fenetre_jeu.blit(mesg, position)

def afficher_message_serpent(tete_serpent):
    global dernier_message, temps_dernier_affichage

    temps_actuel = pygame.time.get_ticks()

    # Vérifier si nous devons mettre à jour le message
    if temps_actuel > temps_min_avant_premier_message and temps_actuel - temps_dernier_affichage > intervalle_message:
        if random.random() < 0.1 or dernier_message is None:
            dernier_message = random.choice(messages_effrayants)
            temps_dernier_affichage = temps_actuel

    # Assurer que dernier_message est défini
    if dernier_message:
        x, y = tete_serpent
        offset_x = random.randint(-100, 100)
        offset_y = random.randint(-100, 100)

        pos_x = x + offset_x
        pos_y = y + offset_y

        # Assurer que les coordonnées du message sont dans l'écran
        pos_x = max(0, min(pos_x, largeur_ecran - 1))
        pos_y = max(0, min(pos_y, hauteur_ecran - 1))

        petite_police = pygame.font.SysFont("bahnschrift", 20)
        mesg = petite_police.render(dernier_message, True, red)
        texte_rect = mesg.get_rect()

        texte_rect.midbottom = (pos_x, pos_y)

        fenetre_jeu.blit(mesg, texte_rect.topleft)


def charger_score_plus_eleve():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def savegarder_score_haut(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def color_random():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def afficher_score(score, score_haut, temps, couleur_texte):
    score_text = police_score.render(f"Score : {score}", True, couleur_texte)
    high_score_text = police_score.render(f"High Score : {score_haut}", True, couleur_texte)
    time_text = police_score.render(f"Time : {temps:.2f} sec", True, couleur_texte)

    fenetre_jeu.blit(score_text, [330, 0])
    fenetre_jeu.blit(high_score_text, [555, 0])
    fenetre_jeu.blit(time_text, [15, 0])

def speed(score):
    return 10 + (score // 5) * 2

def menu_selection_couleur():
    couleurs = [
        (255, 0, 0),   # Rouge
        (0, 255, 0),   # Vert
        (0, 0, 255),   # Bleu
        (255, 255, 0), # Jaune
        (255, 165, 0), # Orange
        (128, 0, 128), # Violet
    ]
    
def dessiner_serpent(taille_bloc, liste_serpent):
    couleur = red if haunted_mode else green
    for segment in liste_serpent:
        pygame.draw.rect(fenetre_jeu, couleur, [segment[0], segment[1], taille_bloc, taille_bloc])

def activer_haunted_mode():
    global haunted_mode
    haunted_mode = True
    try:
        pygame.mixer.music.load(haunted_music)
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Erreur de chargement de la musique hantée: {e}")

def effet_hante():
    fenetre_jeu.fill(blink_color_1)

def main_menu():
    main_active = True
    while main_active:
        fenetre_jeu.fill(black)
        afficher_message("Start Game", white, [largeur_ecran / 2 - 100, hauteur_ecran / 3])
        afficher_message("P pour commencer", white, [largeur_ecran / 2 - 150, hauteur_ecran / 2])
        afficher_message("Q pour quitter", white, [largeur_ecran / 2 - 100, hauteur_ecran / 1.5])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    main_active = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def jeu():
    global haunted_mode
    haunted_mode = False

    try:
        pygame.mixer.music.load('Snake.io Music.mp3')
        pygame.mixer.music.play(-1)
    except pygame.error as e:
        print(f"Erreur de chargement de la musique de fond: {e}")

    game_over = False
    game_close = False

    x1 = largeur_ecran / 2
    y1 = hauteur_ecran / 2

    x1_change = 0
    y1_change = 0

    liste_serpent = []
    longeur_serpent = 1

    food_x = round(random.randrange(0, largeur_ecran - taille_bloc) / taille_bloc) * taille_bloc
    food_y = round(random.randrange(0, hauteur_ecran - taille_bloc) / taille_bloc) * taille_bloc

    score_haut = charger_score_plus_eleve()
    debut_jeu = pygame.time.get_ticks()

    texte_blink_interval = 200
    dernier_changement_texte = pygame.time.get_ticks()
    
    couleur_text = white
    temps_jeu = 0

    dernier_changement_message = pygame.time.get_ticks()
    index_message = 0
    intervalle_message_visible = 2000
    intervalle_message_cache = 2000
    temps_affichage_message = pygame.time.get_ticks()
    message_visible = False

    while not game_over:
        while game_close:
            pygame.mixer.music.stop()
            fenetre_jeu.fill(black)

            if haunted_mode:
                temps_courant = pygame.time.get_ticks()
                if temps_courant - dernier_changement_texte > texte_blink_interval:
                    couleur_text = color_random()
                    dernier_changement_texte = temps_courant
                else:
                    couleur_text = color_random()
            else:
                couleur_text = red

            afficher_message("Tu as perdu! Appuie sur Q-Quitter ou C-Continuer", couleur_text)
            afficher_score(longeur_serpent - 1, score_haut, temps_jeu, couleur_text)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        jeu()
                        return  # Recommencer le jeu sans récursion infinie

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -taille_bloc
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = taille_bloc
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -taille_bloc
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = taille_bloc
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= largeur_ecran or x1 < 0 or y1 >= hauteur_ecran or y1 < 0:
            game_close = True

        if haunted_mode:
            effet_hante()
            temps_courant = pygame.time.get_ticks()
            if temps_courant - dernier_changement_message > intervalle_message_visible:
                dernier_changement_message = temps_courant + intervalle_message_cache
                message_visible = not message_visible
            if message_visible: 
                temps_haunted = pygame.time.get_ticks() - debut_jeu
                tete_serpent = [x1, y1]
                afficher_message_serpent(tete_serpent)
        else:
            fenetre_jeu.fill(black)

        pygame.draw.rect(fenetre_jeu, red if haunted_mode else blue, [food_x, food_y, taille_bloc, taille_bloc])
        serpent_tete = [x1, y1]
        liste_serpent.append(serpent_tete)
        if len(liste_serpent) > longeur_serpent:
            del liste_serpent[0]

        for segment in liste_serpent[:-1]:
            if segment == serpent_tete:
                temps_jeu = (pygame.time.get_ticks() - debut_jeu) / 1000
                game_close = True

        dessiner_serpent(taille_bloc, liste_serpent)
        temps_jeu = (pygame.time.get_ticks() - debut_jeu) / 1000

        if haunted_mode:
            temps_courant = pygame.time.get_ticks()
            if temps_courant - dernier_changement_texte > texte_blink_interval:
                couleur_text = color_random()
                dernier_changement_texte = temps_courant
            else:
                couleur_text = white
        else:
            couleur_text = white

        afficher_score(longeur_serpent - 1, score_haut, temps_jeu, couleur_text)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, largeur_ecran - taille_bloc) / taille_bloc) * taille_bloc
            food_y = round(random.randrange(0, hauteur_ecran - taille_bloc) / taille_bloc) * taille_bloc
            longeur_serpent += 1

            if longeur_serpent - 1 >= score_unlocked and not haunted_mode:
                activer_haunted_mode()

        vitesse_serpent = speed(longeur_serpent - 1)
        horloge.tick(vitesse_serpent)

        if longeur_serpent - 1 > score_haut:
            score_haut = longeur_serpent - 1
            savegarder_score_haut(score_haut)

    pygame.mixer.music.stop()

    pygame.quit()
    quit()

main_menu()
jeu()
