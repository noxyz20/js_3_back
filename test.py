import video

test = video.Video("2.mp4")
frame_array = test.treatement()
print(frame_array)
print(frame_array['data'][0]['id'], frame_array['data'][0]['img'])
test.save_ressource()

#treatment => traite la vidéo, création des keysframes, retourne toute les keyframes
#save_ressource() => Prend toutes les keyframes
#save_ressource([149]) => Ignore toute les keyframes sauf la 149

#Constructeur => nom pour le chemin d'accès, deuxième args = path de la vidéo

