# Procedural-Music
Generates pleasant harmonies by applying musical theory rules

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
    
context = {
    'T': '1|3',
    'S': '2|4|6',
    'D': '5|7',
    'Q': 'S|D'    # Example
}
