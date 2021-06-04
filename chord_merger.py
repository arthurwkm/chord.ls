#pq eu escrevi em camel case e dps desisti?
from pychord import Chord
import json
import re
#vai fazer o merge dos acordes extraídos com o chordino e os pegos do cifraclub
def merge(extracted_file, scraped):
    chord_dictionary = processChords(scraped)
    chord_vectors = []
    print("chord dictionary (made with scraped chords):")
    print(chord_dictionary)
    for chord in chord_dictionary:
        chord_vectors.append(vectorizeChords(chord))
    f = open(extracted_file)#chordChanges.json
    extracted = json.load(f)
    f.close()

    print("chords extracted:")
    print(extracted)
    for i, chord in enumerate(extracted):
        if(chord["estimated_chord"]!= "N"):
            print("for chord: "+chord["estimated_chord"]+" number "+str(i)+"-----------------------------------")
            vectorized_chord = vectorizeChords(chord["estimated_chord"])
        
            extracted[i]["estimated_chord"] = find_closest_vector(vectorized_chord, chord_vectors, chord_dictionary)

    print("chords merged (made by merging extracted and scraped chords):")
    print (extracted)
    return extracted




#vai criar o dicionário de acordes com base na cifra vinda da cifraclub
def vectorizeChords(chord):
    newChordVector = []
    for component in Chord(chord).components():
        velement = numberfyChordComponent(component)
        newChordVector.append(velement)
    return newChordVector




def numberfyChordComponent(component):
    chordValue = 0
    first = True
    for letter in component:
        if first:
            first = False
            if letter == "A":
                chordValue = chordValue + 0
            elif letter == "B":
                chordValue = chordValue + 1
            elif letter == "C":
                chordValue = chordValue + 1.5
            elif letter == "D":
                chordValue = chordValue + 2.5
            elif letter == "E":
                chordValue = chordValue + 3.5
            elif letter == "F":
                chordValue = chordValue + 4
            elif letter == "G":
                chordValue = chordValue + 5
        else:
            if letter == "#":
                chordValue = chordValue + 0.5
            elif letter == "b":
                chordValue = chordValue - 0.5
    #passando o mod para garantir que não vai ter valores negativos ou maiores q 6 (ex: G##)
    return(chordValue % 6)
    



def processChords(scraped):
    with open(scraped, 'r') as file:
        scraped_text = file.read()
    #lines = open( "chordsText.txt", "r" ).readlines()[::2]
    #scraped_text = ''.join(lines)
    scraped_text=scraped_text.split(" ")
    for i, word in enumerate(scraped_text):
        if (word == ''):
            scraped_text[i] = " "
    #o regex abaixo serve para identificar todo tipo de acordes (pode estar incompleto, precisa da ajuda de um profissional de música)
    notes = "[CDEFGAB]"
    accidentals = "(?:#|##|b|bb)?"
    chords = "(?:maj|min|m|sus|aug|dim|add|°)?"
    dim_aum = "(?:\+|\-)?"
    additions = "[0-9]?[0-9]?"
    par = "(?:\((?:#|##|b|bb)?(?:maj|min|m|sus|aug|dim|M|add|°)?[0-9]?[0-9]?/?[0-9]?[0-9]?-?\+?"+"\))?"
    regex = notes + accidentals + chords + dim_aum+ additions +"M?"+dim_aum
    return(list(set(re.findall(r'\b' + regex + "/?" + "(?:"+regex+")?" + par+r'(?!\w)', ''.join(scraped_text)))))




def dist_between_components(comp1, comp2):
    #DISTANCIA DE A PARA G# = MIN(DIST(A,0)+DIST(G#,6), DIST(A,G#))
    return min(abs(comp1-0) + abs(6-comp2), abs(comp1-comp2))




def find_closest_vector(vectorized_chord, chord_vectors, chord_dictionary):
    min_distance = 10000
    index = 0
    for j, vchord in enumerate(chord_vectors):
        distance = 0
        for i, vcomponent in enumerate(vchord):
            if i < min(len(vectorized_chord), len(vchord)):
                #pega a distancia entre dois componentes (na mesma posição) e soma à distancia. repete para n posições onde n é a qtd de componentes do menor acorde
                distance = distance + dist_between_components(vectorized_chord[i], vcomponent)
        #soma à distancia a 
            else:
                if len(vectorized_chord) < len(vchord):
                    distance = distance + dist_between_components(vectorized_chord[0], vcomponent)
                else:
                    distance = distance + dist_between_components(vchord[0], vectorized_chord[i])
        
        if(distance < min_distance):
            min_distance = distance
            print(" the new closest chord is:" + chord_dictionary[j] + " with a distance of: " + str(distance))
            index = j
        
    #transformar estimated_chord em um vetor de notas estimated_chord_vector
    #achar vetor em chord_vectors mais próximo desse vetor
    #lembrando que os acordes estão em dimensões diferentes (existem acordes com 3, 4 ou 5 notas), então o algoritmo tem que ser adaptado
    #soluções: comparar tríades com tríades, apenas
    #          comparar só a quantidades de notas presentes no menor dos dois acordes sendo analisados

    print("  the final closest chord is:" + chord_dictionary[index] + " with a distance of: " + str(min_distance))
    return chord_dictionary[index]
    #transformar estimated_chord em um vetor de notas estimated_chord_vector
    #achar vetor em chord_vectors mais próximo desse vetor
    #lembrando que os acordes estão em dimensões diferentes (existem acordes com 3, 4 ou 5 notas), então o algoritmo tem que ser adaptado
    #soluções: comparar tríades com tríades, apenas
    #          comparar só a quantidades de notas presentes no menor dos dois acordes sendo analisados



    #return estimated_chord
