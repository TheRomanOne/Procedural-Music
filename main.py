from Player import Player
from Theory import *
import random

new_rules = {
    's': '21|43|65',
    'd': '5D|71',
    'A': '11DD',
    'B': '4SD7',
    'C': '3563',
    'E': '1s1'
}

def generate_prog(n=4):
    exp = ['1']
    c_p = [random.choice(keys)]
    # c_p=['F#']
    c_scale = Scale(c_p[0])
    for i in range(n):
        options = c_scale.modulation_options_all(strict=True)

        candidates = c_scale.intersect_chords(options.keys())

        cand = random.choice(candidates)
        if i > 1:
            index = 2 if c_p[-3][-1] == 'm' else 5
            counter = Scale(c_p[-3]).scale_chords[index]
            while cand == c_p[-2] or cand == counter:
                cand = random.choice(candidates)
        c_p.append(cand)
        current_indices = [c_scale.scale_chords.index(x) for x in options[cand]['chords']]

        random.shuffle(current_indices)

        for can in current_indices[:2]:
            exp[-1] = exp[-1] + str(1+can)
        if i < n - 1:
            exp.append('11' if c_p[-1][-1] == 'm' else '12')
        else:
            exp.append('1')
        c_scale = Scale(cand)
    return c_p, exp


scale, exp = generate_prog()
print("Scales", scale)
p = Player()
p.extend_context(new_rules)

p.play_music(scale, exp, False)
p.close()






q=['C', 'Dm', 'Em', 'Am']
q=['G', 'F#°', 'Bm', 'D']
q=['A', 'G#°', 'A', 'C#m']
q=['E', 'B', 'E', 'C#m']
