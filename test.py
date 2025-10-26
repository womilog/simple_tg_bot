from common.database import AudioDatabase

cl = AudioDatabase()
lst = [
    "files/audios/борисов_назв_пастулаты_экономики.mp3",
    "files/audios/мерион_назв_osi.mp3",
]

for path in lst:
    cl.write_audio(path)