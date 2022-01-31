keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
scale_intervals = {
    'M': [2, 2, 1, 2, 2, 2],  # Major chord
    'm': [2, 1, 2, 2, 1, 2]   # Minor chord
}

chords7_types = {
    3: '7',
    4: '(maj)7'
}
triad_types = {
    (3, 3): '°',  # Minor third + minor third
    (3, 4): 'm',  # Minor third + major third
    (4, 3): '',   # Major third + minor third
    (4, 4): '+',  # Major third + major third
}


# "Midi values at https://newt.phys.unsw.edu.au/jw/graphics/notes.GIF"
c3 = 48
c3_octave = 3
# midi instruments.
class Instruments:
    PIANO = 1
    BRASS  = 46
    SOFT_CHELLO  = 49
    WEIRD_ABSTRACT  = 100
    DEVINE  = 52
    BELLS  = 11
    CHELLO  = 48
    GUITAR  = 99
    STRINGS  = 99
    BASS = 5

'''
    Since harmony in music can be expressed in letters,
    music in it's abstract form can be seen as a context
    free language (CFL)
    https://en.wikipedia.org/wiki/Context-free_language
    
    This method allows to create basic musical harmonies
    using letters which makes it easy enough to explore
    and experiment with scales and chord progressions
    
    in the `context` below the numbers 1 ~ 7 represent
    tonal degrees in a 7 note scale (M, m, ...) 
    T - Tonic chords
    S - Sub dominant chords
    D - Dominant chords
    
'''
context = {
    'T': '1|3',
    'S': '2|4|6',
    'D': '5|7',
    'Q': 'S|D'    # Example
}
