from ai_agent.templates import *
from ai_agent.game_handler import *

"""
################# --- Total number of cleaned rows --- #################
 this is the total number of rows that will be cleared due to the addition of two tetriminos.
"""

"""
################# --- Total height of the block --- #################
 the height of the block is the height above the floor of the playing field on which the figure 
is blocked. This is the vertical distance to which a blocked figure would fall if you remove all other occupied squares of 
the playing field and preserve the orientation of the figure. The total blocking height is the sum of the blocking heights 
of two tetriminos.
"""

"""
################# --- Total number of “well” cells --- #################
 a cell-well is an empty cell located above all occupied cells in a column so that its left 
and right neighbors are occupied cells; when determining wells, the walls of the playing field are considered occupied cells. 
The idea is that the well is a structure that is open at the top, closed at the bottom and surrounded by walls on both sides. 
The likelihood of intermittent gaps in the walls of a well means that cell wells do not necessarily occur in a continuous heap within a column.
"""

"""
################# --- The total number of holes in the columns --- #################
 the hole in the column is an empty cell located directly below the occupied cell. 
The floor of the playing field is not compared with the cell above it. There are no holes in the empty columns.
"""

"""
################# --- Total number of transitions in columns --- #################
 a transition in columns is an empty cell adjacent to an occupied cell (or vice versa)
within a single column. The combination of the topmost occupied column block with the empty space above it is not considered 
a transition. Similarly, the floor of the playing field is also not compared with the cell above it. Therefore, there is no 
transition in a completely empty column.
"""

"""
################# --- Total number of transitions in the rows --- #################
 the transition in the rows is an empty cell adjacent to the occupied cell (or vice versa)
within the same row. Empty slots near the walls of the playing field are considered transitions. The total number is calculated for 
all lines of the playing field. However, completely empty lines are not counted in the total number of transitions.
"""


"""
################# --- get_cost --- #################
 uses all cost functions and multiplies result by each cost multiplier to get map_cost
"""


def get_cost(map, cost_multipliers):                       #in a good way    

    # in order to check for transitions we xor the previous scanned parameter with the current one and just count the number of transitions
    nbb = ~BORDER_BOTTOM
    scanner_template = BORDER_TOP
    complete_rows = 0
    #start scanner at correct heigth
    while not (map & scanner_template):
        scanner_template = scanner_template << WIDTH

    prev = map
    res = map
    #get heigths_map
    while 1:
        prev = prev << WIDTH
        res = res | prev
        if not prev&BORDER_BOTTOM:
            break
    
    heigths_map = int(get_bitmap(res),2)&(nbb)
    holes_map = heigths_map^map
    
    #heigth
    heigth = bin(heigths_map).count('1')

    #holes
    holes = 0

    #wells
    wells = 0

    #transitions in rows
    transitions_rows = 0
    prev = None
    empty_collums = 0
    #iteratete WIDTH
    for i in range(WIDTH):
        scanner = BORDER_LEFT << i
        transitions_scanner = map&scanner
        if(scanner & holes_map):
            holes += 1
        if prev:
            transitions_rows += bin((transitions_scanner^(prev<<1))).count('1') 
        prev = transitions_scanner
        if not scanner & map:
            empty_collums  += 1
        #wells
        ##left edge
        if i == 0:
            if bin(scanner & heigths_map).count('1') <  bin((scanner<<1) & heigths_map).count('1') :
                wells += 1
        ##rigth edge
        elif i == WIDTH - 1:
            if bin(scanner & heigths_map).count('1')  <  bin((scanner>>1) & heigths_map).count('1'):
                wells += 1
        ##center
        else:
            if bin(scanner & heigths_map).count('1')  <  bin((scanner>>1) & heigths_map).count('1') and bin(scanner & heigths_map).count('1') < bin((scanner<<1) & heigths_map).count('1'):
                wells += 1

    # transitions in colls
    transitions_colls = 0
    prev = map&scanner_template
    colls_at_max_heigth = bin(prev).count('1')
    scanner = 0
    i = 0
    #iterate HEIGHT
    while 1:
        i += 1
        scanner = scanner_template << (i*WIDTH)
        #complete_rows
        if scanner & map == scanner:
            complete_rows += 1
        scanner = (scanner_template << i*WIDTH)&(map|BORDER_BOTTOM)
        if scanner & BORDER_BOTTOM:
            break
        transitions_colls += bin((scanner^(prev<<WIDTH))).count('1') 
        prev = scanner
    transitions_colls = transitions_colls + colls_at_max_heigth + empty_collums - WIDTH

    #debbug
    #print("cleaned rows", complete_rows )
    #print("heigths", heigth)
    #print("wells", wells)
    #print("holes in collums", holes)
    #print("transitions in collums", transitions_colls)
    #print("transitions in rows", transitions_rows)
    costs = [complete_rows, heigth*min(empty_collums,2), wells, holes, transitions_colls, transitions_rows]
    return sum([cost_multipliers[i]*costs[i] for i in range(len(costs))])





     
