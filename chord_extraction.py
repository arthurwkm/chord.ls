from chord_extractor.extractors import Chordino
from chord_extractor import clear_conversion_cache, LabelledChordSequence




chordino = Chordino(roll_on=1)

# Create an event loop

conversion_file_path = chordino.preprocess('/srv/workspace/climber/G_Em_C_D.ogg')
chords = chordino.extract('/srv/workspace/climber/G_Em_C_D.ogg')
print(chords)
