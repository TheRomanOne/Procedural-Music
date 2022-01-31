import random
from Music import *

class Note:

    def __init__(self, note):
        self.name = note
        self.index = keys.index(note)


    def get_type(self, t):
        return [c + self.index for c in triad_types[t]]

class Chord:
    def __init__(self, notes):
        self.notes = notes
        ln = len(notes)
        ns = [Note(n) for n in notes]
        self.semitones = [n.index for n in ns]

        self.normalize_pitch()
        intervals = [(ns[i + 1].index - ns[i].index) % len(keys) for i in range(ln - 1)]

        self.type = triad_types[tuple(intervals[:2])]
        if ln > 3: # 7th chord
            self.type += chords7_types[intervals[2]]
        self.root = ns[0].name
        self.name = self.root + self.type
        self.chord_notes = ns

    def find_similar(self, c):
        return list(set(self.notes).intersection(c.notes))

    def normalize_pitch(self):
        for i, m in enumerate(self.semitones):
            if i > 0:
                if self.semitones[i-1] > m:
                    self.semitones[i] += 12

    def invert(self, i):
        pass

class Scale:
    def __init__(self, scale, octave=None, context=None, sevens=[]):
        self.context = context
        self.root = scale
        self.scale_type = 'M'
        if 'm' == scale[-1]:
            self.scale_type = 'm'
            self.root = self.root[:-1]
        self.create_scale()
        self.buils_tonal_chords(sevens)
        self.name = scale

    # def modulate_to(self, scale):
    #     prog = self.modulation_options(scale)
    #     print(prog)

    def modulate_to(self, c):
        return self.similar_chords(Scale(c))

    def modulation_options_all(self, strict=False, console_log=False):
        mods = {}
        for k in keys:
            if self.root == k:
                continue
            def _parse_scales(s, ns):
                r={}
                if len(ns) > 0:
                    if strict:
                        if self.name in ns: ns.remove(self.name)
                        if s.name in ns: ns.remove(s.name)

                    if not (strict and len(ns) > 4):
                        r = {
                            'chords': ns,
                            'indices': [1 + s.scale_chords.index(x) for x in ns]
                        }
                return r

            major = Scale(k)
            minor = Scale(k + 'm')

            maj_c = _parse_scales(major, self.similar_chords(major))
            min_c = _parse_scales(minor, self.similar_chords(minor))

            # m = {}
            if len(maj_c) > 0: mods[k] = maj_c
            if len(min_c) > 0: mods[k+'m'] = min_c

            # if len(m.keys()) > 0:
            #     mods[k] = m

        if console_log:
            p=''
            for k in mods.keys():
                p+=f'\n\n--> {k}'
                key = mods[k]
                for t in key.keys():
                    p += f'\t  {key[t]}'
            print("Diatonic chords", self.scale_chords)
            print(p)

        return mods

    def intersect_chords(self, chords):
        return list(set(self.scale_chords).intersection(chords))

    def similar_chords(self, scale):
        return self.intersect_chords(scale.scale_chords)

    def similar_notes(self, c):
        return list(set(self.notes.keys()).intersection(c.notes.keys()))

    def create_scale(self):
        intervals = scale_intervals[self.scale_type]
        i = keys.index(self.root)
        last = 0
        self.scale_notes = [self.root]
        self.notes = {}
        self.notes[self.root] = Note(self.root)
        for n in intervals:
            last += n
            index = (last + i) % len(keys)
            k = keys[index]
            self.scale_notes.append(k)
            if k not in self.notes.keys():
                self.notes[k] = Note(k)

    def _build_chord(self, sn, i, n, t=''):
        third = sn[(i + 2) % len(sn)]
        fifth = sn[(i + 4) % len(sn)]
        chord = [n, third, fifth]

        if t == '7': # Add a seventh to the chord
            chord.append(sn[(i + 6) % len(sn)])
        return Chord(chord)

    def buils_tonal_chords(self, sevens=[]):
        '''
        :param sevens: scale
        :return:
        '''
        self.chords = []
        self.chords_midi = []
        sn = self.scale_notes
        for i, n in enumerate(sn):
            t = '7' if len(sevens) > 0 and (i+1) in sevens else ''
            c = self._build_chord(sn, i, n, t)
            self.chords.append(c)

        self.scale_chords = [c.name for c in self.chords]

    def _choose(self, l):
        return l[random.randrange(0, len(l))]

    def set_expression(self, song):
        self.chord_progression = []
        self.parse_expression(song)


    def parse_expression(self, s, tab=''):
        if self.context is None:
            raise Exception('Context missing')
        _s = s.split('|')
        _s = self._choose(_s)
        for n in _s:
            if n == '_':
                continue
            if n.isnumeric():
                c = self.chords[int(n)-1]
                self.chord_progression.append(c)
            else:
                state = self.context[n]
                self.parse_expression(state, tab + '---')

    def get_chord_progression(self): return self.chord_progression


    def get_chord_names(self): return [c.name for c in self.chord_progression]