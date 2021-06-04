from os import name
from typing import Any
from chord_extractor.extractors import Chordino
import json
import chord_merger
import name_song
import chords_scraper
import sys
import PySimpleGUI as sg
import os.path

chordino = Chordino(roll_on=1)
# First the window layout in 2 columns
cur_page = 0
page_count = 0

file_list_column = [

    [

        sg.Text("Audio Folder"),

        sg.In(size=(20, 1), enable_events=True, key="-FOLDER-"),

        sg.FolderBrowse(),
        

    ], [sg.Text("Select an audio file from the list below:")],

    [

        sg.Listbox(

            values=[], enable_events=True, size=(35, 20), key="-FILE LIST-"

        )

    ],

]


# For now will only show the name of the file that was chosen

image_viewer_column = [

    [sg.Text(text="Chords Extracted:")],

    [sg.Multiline(size=(20, 20), key="-TOUT-")],

    

]

chord_viewer_column = [

    [sg.Text(text="Chords + Lyrics Scraped:", key="-STITLE-", )],

    [sg.Multiline(size=(50, 20), key="-TOUT2-")],
    #[sg.Button("Prev"),sg.Button("Next")],
    
    
    
    #[sg.Image(key="-IMAGE-")],


]


# ----- Full layout -----

layout = [

    [

        sg.Column(file_list_column),

        #sg.VSeperator(),

        #sg.Column(image_viewer_column),
        sg.Column(chord_viewer_column),

    ]

]


window = sg.Window("Chord.ls", layout, resizable=True)


# Run the Event Loop

while True:

    event, values = window.read()

    
    if event == "Exit" or event == sg.WIN_CLOSED:

        break

    # Folder name was filled in, make a list of files in the folder

    if event == "-FOLDER-":

        folder = values["-FOLDER-"]

        try:

            # Get list of files in folder

            file_list = os.listdir(folder)

        except:

            file_list = []


        fnames = [

            f

            for f in file_list

            if os.path.isfile(os.path.join(folder, f))

            and f.lower().endswith((".mid", ".wav", ".mp3", ".ogg"))

        ]

        window["-FILE LIST-"].update(fnames)

    elif event == "-FILE LIST-":  # A file was chosen from the listbox

        try:

            filename = os.path.join(

                values["-FOLDER-"], values["-FILE LIST-"][0]

            )

            chords_extracted_file = "chordChanges.json"
            chords_scraped_file = "chordsText.txt"
            chords_merged_file = "chordsMerged.json"


            #splitting into guitar/other sound to make the chord extraction easier
            #FILENAME = /PATH/OTHER.WAV
            
            # chord extraction 
            conversion_file_path = filename #chordino.preprocess(filename)
            chords = chordino.extract(conversion_file_path)
            #jsonification
            sys.stdout = open(chords_extracted_file, "w")
            #chords = json.dumps(chords)
            #print(chords)
            print("[")
            for i, chordChange in enumerate(chords):
                if i == len(chords)-1:
                    print("  {\n  \"estimated_chord\": "+ "\""+chordChange.chord+ "\"" + ",\n  \"timestamp\": "+ str(chordChange.timestamp) + "\n  }")
                else:
                    print("  {\n  \"estimated_chord\": "+ "\""+chordChange.chord+"\"" + ",\n  \"timestamp\": "+ str(chordChange.timestamp) + "\n  },")            
            print("]")
            sys.stdout.close()
            #update the multilines with the gathered data
            #window["-TOUT-"].update(open(chords_extracted_file).read())
            #if the song is recognized, scrape for the chords online
            song_name = name_song.name_song(filename)
            song_artist = name_song.artist_song(filename)
            recognized = True
            if song_name == "A música não foi reconhecida":
                recognized = False

            if recognized == True:
                sys.stdout = open(chords_scraped_file, "w")
                url = chords_scraper.scrape_chords(song_name, song_artist)
                sys.stdout.close()

                window["-TOUT2-"].update(open(chords_scraped_file).read())

            else:
                #clean the file if this song will not use it
                sys.stdout = open(chords_scraped_file, "w")
                print("A música não foi reconhecida!")
                sys.stdout.close()
                #update image with "musica não reconhecida!"
                #window["-IMAGE-"].update(filename='not_recognized.png')
                window["-TOUT2-"].update(open(chords_scraped_file).read())
                

            #merge chords from scraped and extracted files to make a better document
            #(one that features timestamps AND correct chords taken from the internet)
            #put the log of the merging of files in the "chordsMerge.txt"
            sys.stdout = open("chordsMerge.txt", "w")
            merged_chords = chord_merger.merge(chords_extracted_file, chords_scraped_file)
            sys.stdout.close()
            #jsonifying the merged chords
            merged_chords = json.dumps(merged_chords)
            sys.stdout = open(chords_merged_file, "w")
            print(merged_chords)
            sys.stdout.close()

            
            
    

        except:
            
            pass
                   


window.close()
