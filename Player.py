from Theory import *
import pygame.midi
import time, threading


class Player:
    def __init__(self, pitch_focus_range=[48, 60]):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.pitch_focus_range = pitch_focus_range
        self.context = context
        self.speed = 1.7

    def extend_context(self, c):
        self.context = {**self.context, **c}

    def filter_sound(self, sound):
        # Keep pitches around a pitch range (not strict limit)
        _s = []
        for s in sound:
            if s < self.pitch_focus_range[0]:
                _s.append(s+12)
            elif s > self.pitch_focus_range[1]:
                _s.append(s-12)
            else:
                _s.append(s)
        return _s

    def play_note(self, note, duration):
        self.play_chord([note], duration)

    def play_chord(self, notes, duration):
        # To play a note it needs to be turned on
        # and then turned off after some time

        for i, t in enumerate([self.player.note_on, self.player.note_off]):
            for n in notes:
                v = 127
                t(n, v)
            time.sleep(duration)

    def play_progression(self, prog):
        ''' Plays a chord progression.
            The progression is a list of tuples
            c = (n, d)
            where:
                n = note or list of notes (chord)
                d = inverted duration -
                    4 = a quarter note
                    8 = an eighth note
                    ...
                '''


        for i, c in enumerate(prog):
            f = self.play_chord if type(c[0]) == list else self.play_note
            f(c[0], 1/c[1])

    def play_instrument(self, inst, prog):
        # print(list(instruments.keys()))
        self.player.set_instrument(inst)
        self.play_progression(prog)

    def play_style1(self, c):
        print("play_style1")
        self.play_instrument(Instruments.PIANO, [
            ([_c - 12 for _c in c[:-1]], 3*self.speed),
        ])
        self.play_instrument(Instruments.STRINGS, [
            (c[1:], 3*self.speed),
            ([c[0] - 12, c[-1]], 3*self.speed),
            (c, 9*self.speed),
        ])
        self.play_instrument(Instruments.PIANO, [
            (c[0], 9*self.speed),
            (c[1]-12, 9*self.speed),
        ])

    def play_style2(self, c):
        print("play_style2")
        self.play_instrument(Instruments.PIANO, [
            ([_c - 12 for _c in c[:-1]], 3 * self.speed),

        ])
        self.play_instrument(Instruments.STRINGS, [
            ([c[0]-12, c[-1]], 3 * self.speed),
            ([_c-12 for _c in c[1:]], 3 * self.speed),
            (c, 3 * self.speed),
        ])

    def play_style3(self, c):
        print("play_style3")
        self.play_instrument(Instruments.PIANO, [
            (c[1] - 24, 3*self.speed),
            (c, 3*self.speed),
            (c[1] - 12, 3*self.speed),
            (c, 3*self.speed)
        ])

    def play_style4(self, c):
        print("play_style4")
        self.play_instrument(Instruments.STRINGS, [
            (c[1:], 3 * self.speed),
        ])
        self.play_instrument(Instruments.PIANO, [
            ([_c-12 for _c in c[1:]], 3 * self.speed),
        ])
        self.play_instrument(Instruments.STRINGS, [
            (c[0], 3 * self.speed),

        ])
        self.play_instrument(Instruments.PIANO, [
            (c[1:], 3 * self.speed),
        ])

    def modulate_to_pitch(self, c, p):
        s = sum(c)
        print('')


    def play_piece(self, prog, invert_chords=True, log=True):
        prog_names = [c.name for c in prog]

        print(f"Chord progression: {prog_names}\n")
        styles = [self.play_style1, self.play_style2, self.play_style3, self.play_style4]
        for i, c in enumerate(sng):
            chord_name = prog_names[i]
            p = prog[i]
            notes = ', '.join(p.notes)

            if log:
                print(f'{chord_name}: {notes}', f'| inv {p.inversion}' if invert_chords else None)
            random.shuffle(c)
            # c = self.filter_sound(c)
            # self.play_style1(c)
            c = self.modulate_to_pitch(c, c3)
            styles[self.play_count % len(styles)](c)
            self.play_count += 1

    def play_music(self, scales, song=None, log=True):
        # Plays each piece in a certain scale
        self.play_count = 0

        if song is None:
            song = ['1'] * len(scales)
        for i, k in enumerate(scales):
            scl = Scale(k, octave=3, context=self.context)
            s = song[i]
            if log:
                print("\n\n===== >> Key of", k)
                print("Notes:", scl.scale_notes)
                print(f"Chords: {scl.scale_chords}\n")
            scl.set_expression(s)
            c_prog = scl.get_chord_progression()

            self.play_piece(c_prog, log=log)

    def close(self):
        del self.player
        pygame.midi.quit()
