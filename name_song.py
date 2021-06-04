from ShazamAPI import Shazam

#try to find the name/artist of the song based on the api's recognition
def name_song(path):
    try:
        mp3_file_content_to_recognize = open(path, 'rb').read()
        shazam = Shazam(mp3_file_content_to_recognize)
        recognize_generator = shazam.recognizeSong()
        for i, response in enumerate(next(recognize_generator)):
            if i > 0:
                return (response['track']['title'])

    except:
        return ("A música não foi reconhecida")

def artist_song(path):
    try:
        mp3_file_content_to_recognize = open(path, 'rb').read()
        shazam = Shazam(mp3_file_content_to_recognize)
        recognize_generator = shazam.recognizeSong()
        for i, response in enumerate(next(recognize_generator)):
            if i > 0:
                return (response['track']['subtitle'])

    except:
        return ("A música não foi reconhecida")
        

