import datetime
from plexapi.server import PlexServer

L = [("The Batman","2024-09-23 18:51:14"),("1917","2023-12-27 06:51:14"), ("About Kim Sohee","2024-02-25 20:25:42"),("Anatomie d'une chute","2024-02-25 20:23:21"),("Avengers","2024-01-05 09:43:33"),("Avengers : Endgame","2023-12-30 04:21:59"),("Avengers : Infinity War","2024-01-05 02:48:41"),("Barbie","2023-12-25 17:56:53"),("Beasts of No Nation","2024-03-11 00:36:23"),("Beau Is Afraid","2024-02-05 21:08:03"),("Challengers","2024-05-21 18:24:02"),("Citizenfour","2023-12-30 17:25:40"),("Civil War","2024-05-24 15:27:57"),("Django Unchained","2023-12-29 16:31:07"),("Don't Look Up : Déni cosmique","2023-12-27 01:24:39"),("Dream Scenario","2024-02-05 21:01:33"),("Dune : Deuxième partie","2024-04-08 19:41:47"),("Dune : Première partie","2023-12-29 13:30:50"),("Edge of Tomorrow","2023-12-29 13:12:56"),("Fight Club","2023-12-27 01:41:59"),("Gladiator","2023-12-25 22:04:09"),("Godzilla Minus One","2024-06-02 02:25:50"),("Godzilla x Kong : Le Nouvel Empire","2024-05-21 18:23:54"),("Gone Girl","2024-01-22 14:52:59"),("Hercule","2024-03-04 21:06:16"),("Hunger Games : La Ballade du serpent et de l'oiseau chanteur","2024-02-25 18:18:47"),("Icare","2024-08-04 02:01:48"),("Inception","2023-12-28 20:26:06"),("Inglourious Basterds","2024-01-05 02:44:55"),("Insomnia","2023-12-25 21:34:07"),("Interstellar","2023-12-24 17:13:24"),("John Wick : Chapitre 4","2024-08-30 00:50:27"),("Joker","2023-12-29 16:13:34"),("Killers of the Flower Moon","2023-12-22 23:00:13"),("King’s Land","2024-06-23 15:13:12"),("Land of Bad","2024-05-21 18:23:57"),("Le Cercle des neiges","2024-01-05 02:20:06"),("Le Discours d'un roi","2023-12-25 22:15:42"),("Le Hobbit : La Bataille des cinq armées","2023-12-31 18:07:36"),("Le Hobbit : La Désolation de Smaug","2023-12-31 18:06:10"),("Le Hobbit : Un voyage inattendu","2023-12-31 17:53:30"),("Le Monde après nous","2024-03-30 03:42:48"),("Le Parrain","2023-12-27 01:59:25"),("Le Parrain 2","2023-12-27 02:16:46"),("Le parrain, 3e partie","2023-12-27 02:29:48"),("Le Prestige","2024-01-26 20:29:34"),("Le Seigneur des anneaux : La Communauté de l'anneau","2023-12-24 19:30:33"),("Le Seigneur des anneaux : Le Retour du roi","2024-01-03 14:21:03"),("Le Seigneur des anneaux : Les Deux Tours","2024-01-03 14:24:48"),("Le Talentueux M. Ripley","2024-09-12 14:43:03"),("Les Gardiens de la Galaxie : Volume 3","2023-12-26 21:47:56"),("Les Infiltrés","2023-12-27 01:20:56"),("Les Trois Mousquetaires : D'Artagnan","2024-04-04 16:39:18"),("Les trois mousquetaires : Milady","2024-04-04 16:36:26"),("Looper","2024-02-02 22:27:34"),("Lord of War","2024-01-26 19:10:08"),("Madame Web","2024-04-25 18:39:13"),("Mademoiselle","2024-05-21 18:22:36"),("Memento","2023-12-25 21:15:08"),("Mission : Impossible - Dead Reckoning Partie 1","2024-01-10 09:04:46"),("Monty Python - le sens de la vie","2024-08-11 15:55:13"),("Monty Python : La vie de Brian","2024-08-11 15:55:10"),("Monty Python : Sacré Graal !","2024-08-11 15:55:08"),("Napoléon","2024-01-09 19:03:35"),("Once Upon a Time in... Hollywood","2023-12-27 04:36:14"),("Oppenheimer","2023-12-21 02:14:42"),("Past Lives - Nos vies d’avant","2024-02-03 05:14:10"),("Pauvres créatures","2024-02-28 22:20:10"),("Premier Contact","2023-12-23 02:56:12"),("Prisoners","2024-01-07 03:44:51"),("Rebel Moon - Partie 1 : Enfant du feu","2023-12-23 20:31:20"),("Rebel Moon – Partie 2 : L'Entailleuse","2024-04-26 15:40:18"),("Seul sur Mars","2023-12-25 22:56:40"),("Seven","2023-12-27 02:01:44"),("Shutter Island","2023-12-27 01:10:51"),("Sicario","2023-12-29 12:41:00"),("Sicario : La Guerre des cartels","2023-12-29 13:06:16"),("Tenet","2024-01-26 16:04:09"),("The Fall Guy","2024-05-24 15:27:58"),("The Killer","2024-01-06 22:47:39"),("The Marvels","2023-12-29 23:36:47"),("Top Gun : Maverick","2023-12-25 18:03:55"),("War Dogs","2024-01-26 19:08:37"),("Whiplash","2023-12-27 02:32:08"),("Zero Dark Thirty","2024-01-01 16:29:11"),("Zodiac","2024-01-26 19:08:37")]

result_dict = {title: new_date for title, new_date in L}

# Printing the resulting dictionary

# Initialize the Plex server connection
baseurl = 'http://192.168.1.15:32400/'
token = '7CsKhedPzzMpN992xcdc'
plex = PlexServer(baseurl, token)

def print_added_dates_2():
    # Fetching all library sections
    sections = plex.library.sections()
    
    for section in sections:

        if section.title == "diego-Films":
            print(f"\nSection: {section.title}")

            # Fetching all items in the section
            for item in section.all():
                # Print the title and added_at date
                # print(f"AVANT - {item.title}: {result_dict[item.title]}")
                new_date_unix = int(datetime.datetime.strptime(result_dict[item.title], '%Y-%m-%d %H:%M:%S').timestamp())
                
                # Update the addedAt date using editAddedAt with Unix timestamp
                item.editAddedAt(new_date_unix)
                # print(f"APRES - {item.title}: {item.addedAt}")
    print("DONE.")

if __name__ == "__main__":
    # print_added_dates()
    print_added_dates_2()