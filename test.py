import video

test = video.Video("toto", "2.mp4")
frame_array = test.treatement()
test.save_ressource([149])

#treatment => traite la vidéo, création des keysframes, retourne toute les keyframes
#save_ressource() => Prend toutes les keyframes
#save_ressource([149]) => Ignore toute les keyframes sauf la 149

#Constructeur => nom pour le chemin d'accès, deuxième args = path de la vidéo