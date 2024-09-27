SELECT 
    metadata_items.id, 
    metadata_items.title, 
    DATETIME(metadata_items.originally_available_at, 'unixepoch') AS aired_date,
    DATETIME(metadata_items.added_at, 'unixepoch') AS added_at,
    (JULIANDAY('now') - JULIANDAY(DATETIME(metadata_items.added_at, 'unixepoch'))) * 1440 AS minutes_since_added,
    metadata_items.library_section_id
FROM 
    metadata_items
WHERE 
    metadata_items.library_section_id IS NOT NULL
    AND metadata_items.title IN ("Top Gun : Maverick", "Mission : Impossible - Dead Reckoning Partie 1", "Zodiac", "Zero Dark Thirty", "Whiplash", "War Dogs", "Le Cercle des neiges", "Sicario", "Shutter Island", "Seven", "Once Upon a Time in... Hollywood", "Memento", "The Marvels", "Seul sur Mars", "Le Discours d'un roi", "Joker", "Insomnia", "Inglourious Basterds", "Les Gardiens de la Galaxie : Volume 3", "Gone Girl", "Le Parrain", "Le Parrain 2", "Le Parrain 3", "Gladiator", "Edge of Tomorrow", "Django Unchained", "Citizenfour", "Barbie", "Avengers : Endgame", "Avengers : Infinity War", "Avengers", "Le Monde après nous", "Don't Look Up : Déni cosmique", "Les trois mousquetaires : Milady", "Les Trois Mousquetaires : D'Artagnan", "Madame Web", "Lord of War", "Dream Scenario", "The Killer", "Inception", "Le Hobbit : La Bataille des cinq armées", "Rebel Moon – Partie 2 : L'Entailleuse", "Tenet", "About Kim Sohee", "Sicario : La Guerre des cartels", "1917", "Les Infiltrés", "Le Hobbit : La Désolation de Smaug", "Le Seigneur des anneaux : Le Retour du roi", "Beasts of No Nation", "Le Seigneur des anneaux : Les Deux Tours", "Le Prestige", "Dune : Première partie", "Le Hobbit : Un voyage inattendu", "Fight Club", "Godzilla x Kong : Le Nouvel Empire", "Challengers", "King’s Land")  -- Replace ... with the rest of your IDs
	AND metadata_items.library_section_id = 12
ORDER BY 
	metadata_items.title ASC;
