from ai_agent.templates import *

def get_bitmap(b):
    st = ""
    for y in range(HEIGHT):
        st += (''.join(['01'[ (b>>(y*WIDTH+x))&1  ] for x in range(WIDTH)]))    #print any 8x30 bitmap
    return st[len(st)-WIDTH::-1]
def print_bitmap(b):
    for y in range(HEIGHT):
        print(' '.join(['01'[ (b>>(y*WIDTH+x))&1  ] for x in range(WIDTH)]))    #print any 8x30 bitmap
    print()

#piece -> (Type, index(rotation, offset), shift_amount)
#in templates.py we have all information need about the pieces,
#you only need to know what kind of piece it is and at what stage of its rotation it is at,
#then you just need to shift its template to represent it on the desired location


#we always need to shift in reverse since we display the bitmap  in reverse, in order to follow the game's coordinate system:
#bit number(on display): (8x30)
#0 1 2 3 4 5 6 7
#8 9 10 ....
sh_r = lambda b, amount: b<<amount                          #shift rigth
sh_l = lambda b, amount: b>>amount                          #shift left
sh_b = lambda b, amount: b<<(amount*WIDTH)                      #shift down, as you can see from the exemple above, in order to get the bit in position 1 to podition 9 you would need to shift in left by 8(field size)
sh_t = lambda b, amount: b>>(amount*WIDTH)                      #shift up (same logic as shift down)

#shift piece by amount
shp_r = lambda p, amount: (p[0], p[1], p[2]+amount)         #shift piece right (update piece[2] (shift_amount))
shp_l = lambda p, amount: (p[0], p[1], p[2]-amount)         #shift piece left (update piece[2] (shift_amount))
shp_b = lambda p, amount: (p[0], p[1], p[2]+WIDTH*amount)       #shift piece down (update piece[2] (shift_amount))
shp_t = lambda p, amount: (p[0], p[1], p[2]-WIDTH*amount)       #shift piece up (update piece[2] (shift_amount))

def print_piece(piece):
    base_bit_template = PIECES[piece[0]][piece[1]]          #gets basic template from templates.PIECES, using rotation index
    print_bitmap(base_bit_template << piece[2])             #shifts piece by riquired amount, templates will always be drawn near the origin (x=1,y=1)

# uses a row or a collum of '1' (similar to templates.BORDER*) as a scanner (using shift operation to move it) and &(and) operator
# to check for colisions on both axis, increasing its count any time it collides with the piece    
def get_piece_size(piece):
    base_template = PIECES[piece[0]][piece[1]]              #get piece template
    return get_template_size(base_template)

def get_template_size(template):
    base_template = template
    scanner_collum = int(('0'*(WIDTH-1)+'1')*4,2)                    #templates are shifted to the top-left corner, and since no piece is bigger than 4 in size, we only need a 4*'1' scanner
    scanner_row = 15                                        #same applies 15 = 0b1111
    #initiallise counters
    count_y = 0
    count_x = 0
    #scan x axis
    while scanner_collum & base_template:                   #while scanner is collides with piece
        count_x += 1                                        #count increments
        scanner_collum = sh_r(scanner_collum, 1)            #then scanner moves to the rigth
    #scan y axis
    while scanner_row & base_template:                      #while scanner is collides with piece
        count_y += 1                                        #count increments
        scanner_row = sh_b(scanner_row, 1)                  #then scanner moves down
    return (count_x, count_y)                               # returns (size, heigth)

#tranforms coord array from server into bitmap
def coord_to_bitmap(array):
    b = 0                                                   #initialise bitmap
    for item in array:
        #shifts left '1' (y-1)*8+(x-1) times
        #we decrese each coord by 1 since we dont need to draw or use bits for walls
        #y axis is incremented by 8, since in order to move down a bit we need to shitf it 8 times,
        #x axis is incremented by 1, since in order to move a bit to the right we need to only shift it once
        #|(or) operator makes sure all the bits get added
        #the same tactic is used in order to draw a piece into the game_map (piece|game_map)
        b |= 1<<((item[1]-1)*WIDTH+(item[0]-1))                 
    return b

def next_piece_to_bitmap(array):
    b = 0                                                   #initialise bitmap
    for item in array:
        #shifts left '1' (y-1)*8+(x-1) times
        #we decrese each coord by 1 since we dont need to draw or use bits for walls
        #y axis is incremented by 8, since in order to move down a bit we need to shitf it 8 times,
        #x axis is incremented by 1, since in order to move a bit to the right we need to only shift it once
        #|(or) operator makes sure all the bits get added
        #the same tactic is used in order to draw a piece into the game_map (piece|game_map)
        b |= 1<<((item[1])*WIDTH+(item[0]))                 
    return b

#takes a piece bitmap (the piece can be in any position)
#shifts the piece to the top-left corner,
#returns its integer value, and and the amount of shitfs done
#pieces always spawn in the middle of the screen, meaning that
#by shifting it to the top-left corner we only shift in one direction
#so in order to get the original position back, we only need to get
#its template and shift it back the oposite direction, the same amount
def getTemplateKey(piece_map):
    shcount = 0
    while not (piece_map & BORDER_TOP):                         #shift up
        piece_map = sh_t(piece_map, 1)
        shcount += WIDTH                                        #increment by 8 (same rule as before)

    while not (piece_map & BORDER_LEFT):                        #shift left
        piece_map = sh_l(piece_map, 1)
        shcount += 1                                            #only need to increment by 1

    return (piece_map, shcount)

#uses the functions described before to direcly go from
#an array of coords to a piece tuple(Type, index(rotation, offset), shift_amount)
def coords_to_piece(array, shift=False):
    if shift:
        piece_map = next_piece_to_bitmap(array)
    else:
        piece_map = coord_to_bitmap(array)                           #gets raw bitmap
    
    template, sh_amount = getTemplateKey(piece_map)              #simplify to base template and shift amount
    piece_type = TEMP_TO_KEY[template]                           #use templates.TEMP_TO_KEY to get piece type

    return (piece_type, PIECES[piece_type].index(template), sh_amount)

#all rotation templates are already pre hard coded
#you can get tem  in tempates.PIECES    
#if you want to rotate the piece once you just need to get
#the next template in the current PIECES list (templates.PIECES[piece[0]][piece[1]+1%len(current array(PIECES[piece[0]]))])

#since all templates are shifted to the top-left corner sometimes we need to take
#into acount an offset in order to draw the piece in the correct position
#if you want to rotate between positions with diferent offsets you need to
#subtract the current offset from the destination offset
#offest = destination_offset - current_offset
#we can get all offsets from templates.ROTATION_OFFSET, using the same index used for the piece template
#these are hard coded
def rotate(piece, amount=1):
    prev_idx = piece[1]                                             #current_offset
    new_idx = (piece[1]+amount)%len(PIECES[piece[0]])               #destination off_set
    offset = ROTATION_OFFSET[piece[0]][new_idx] - ROTATION_OFFSET[piece[0]][prev_idx] 

    return (piece[0], new_idx, piece[2]+offset)                     #(sane type, new rotation index, shift_amout + offset)




def piece_to_bitmap(piece):
    return PIECES[piece[0]][piece[1]] << piece[2]

