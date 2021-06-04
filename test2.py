from pychord import Chord


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


print(vectorizeChords("Am/C"))