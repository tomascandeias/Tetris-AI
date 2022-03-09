#hard coded templates for faster search
WIDTH = 8
HEIGHT = 30
BORDER_TOP = int('1'*WIDTH,2)                           #255 / 0b11111111

#since we display bits reversed in order to match the coord system,
#this really represents
#10000000
#10000000
#10000000
#  ...
BORDER_LEFT = int('00000001'*HEIGHT,2)

BORDER_BOTTOM = BORDER_TOP<<(HEIGHT-1)*WIDTH

#in order to obtain this values we converted the 
#template bit maps (shifted to the top-left corner) to integer value:
#Ex: PIECES['O'][0]
# +     01234567
#
#0*8    11000000
#1*8    11000000
#2*8    00000000
#3*8    00000000
#  ...
#PIECES['O'][0] = 0b1100000011 = 771
PIECES = {
    'S': [774, 131841],
    'Z': [1539, 66306],
    'I': [16843009, 15],  
    'O': [771],
    'J': [1793, 65795, 1031, 197122],
    'L': [1796, 131587, 263, 196865],
    'T': [1794, 66305, 519, 131842]
}

#compared rotations to this image and shape.py to see
#how much rows and collums pieces needed to be offseted
#afer a rotation, always remember, moving down means shifting
#in increments of 8 and right in increments of 1
#https://static.wikia.nocookie.net/tetrisconcept/images/3/3d/SRS-pieces.png/revision/latest?cb=20060626173148

#Ex:
#['T'][0]   ['T'][1]
#without offset
#010        100
#111    >   110
#000        100
#with offset
#010        010
#111    >   011
#000        010
ROTATION_OFFSET = {
    'S': [0, 0],
    'Z': [0, 0],
    'I': [2, WIDTH],   
    'O': [0],
    'J': [0, 1, WIDTH, 0],
    'L': [0, 1, WIDTH, 0],
    'T': [0, 1, WIDTH, 0]
}


#reverse dict of PIECES for faster template recognition
TEMP_TO_KEY = {
    774: 'S',
    131841: 'S',
    1539: 'Z',
    66306: 'Z',
    16843009: 'I',
    15: 'I',
    771: 'O',
    1793: 'J',
    65795: 'J',
    1031: 'J',
    197122: 'J',
    1796: 'L',
    131587: 'L',
    263: 'L',
    196865: 'L',
    1794: 'T',
    66305: 'T',
    519: 'T',
    131842: 'T'
}
