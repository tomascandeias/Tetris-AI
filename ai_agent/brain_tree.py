from ai_agent.templates import *
from ai_agent.game_handler import *
from ai_agent.cost_functions import *

class SearchNode:
    def __init__(self, data, t,cost=0): 
        self.cost = cost
        #self.depth = depth
        self.data = data
        self.t = t
        self.parent = None
        self.children = []
        if self.t == "piece":
            self.leafs = []
    
    #sorted insert, in order to get lowest cost on index = 0
    #order only matter when indexing map nodes
    def add_child(self, child):
        
        child.parent = self
        if not child.t == 'map':
            self.children.append(child)
        else:
            insert_index = insert(child, self.children)
            self.children.insert(insert_index, child)
            #pointer to piece specific leafs
            insert_index = insert(child, self.parent.leafs)
            self.parent.leafs.insert(insert_index, child)



                


def print_tree(root, count = 0):
    gap = "                     "
    print(gap*count + root.t, root.data)
    for rot in root.children:
        print(gap*count + "   "+ rot.t, rot.data)
        for m in rot.children:
            print(gap*count + "         " + "map: " + str(m.cost))
            #print(gap*count + "         " + str(m.t))
            #print(gap*count + "         data: " + str(m.data))
            #print(gap*count + "         cost: " + str(m.cost))
            #print()
            if m.children:
                print_tree(m.children[0], count+1)




#############################tree version

#find all moves for a piece template (single rotation)
def find_template_piece_moves(piece_template, game_map, parent_node, cost_multipliers):
    piece_template_size = get_template_size(piece_template)[0]      #get piece size
    possible_positions = []
    for i in range(WIDTH + 1 - piece_template_size):                #iterate possible x_axis positions (i represents the amount of shifts required to get to a position)
        simulation_piece = sh_r(piece_template, i)                  #get correct piece position by shifting template(always start on top-left corner)
        #check for colision
        while not simulation_piece & (game_map | BORDER_BOTTOM):    #&(and) operator to check for colisions with game_map |(or) BORDER_BOTTOM
            simulation_result = (simulation_piece | game_map)       #|(or) operator to get bitmap with both the piece and the game_map
            simulation_piece = sh_b(simulation_piece, 1)            #simulation_piece starts in any top position, and needs to get lowered each time we iterate to check for colisions
        possible_positions.append(simulation_result)                #save the value, before iterating, we want the resulting game_map the move before the colision
        map_node = SearchNode(data=simulation_result, t='map', cost=get_cost(simulation_result, cost_multipliers))
        parent_node.add_child(map_node)
    return possible_positions


#find all possible moves for a piece type (all rotations)
def generate_base_tree(piece_type, game_map, cost_multipliers):
    templates = PIECES[piece_type]                                  #get template list from templates.PIECES
    root = SearchNode(data=piece_type, t="piece")
    
    for i in range(len(templates)):
        
        rot_ind = SearchNode(data=i, t="rotation_index")
        root.add_child(rot_ind)
        find_template_piece_moves(templates[i], game_map, rot_ind,  cost_multipliers)
        
    return root


def get_tree_depth(node):
    if not node.children:
        return -1
    if node.t=="piece":
        return get_tree_depth(node.leafs[0])+1
    return get_tree_depth(node.children[0])


 #insert new piece into tree
def insert_next_piece_to_tree(root, piece_type, cost_multipliers):
    depth = get_tree_depth(root)
    minimum = None
    res = SearchNode(None,None)
    

    #generate new tree from the best 3 positions from current piece
    if depth == 0:
        for map_node in root.leafs[:3]:
            map_node.add_child(generate_base_tree(piece_type, map_node.data, cost_multipliers))
            minimum =  map_node.children[0].leafs[0]
            if not res.t:
                res = minimum 
            if res.cost > minimum.cost:
                res = minimum

    #generate new tree from the best 2 positions from next piece 1
    if depth == 1:
        for l1 in root.leafs[:3]:
            for map_node in l1.children[0].leafs[:2]:
                map_node.add_child(generate_base_tree(piece_type, map_node.data, cost_multipliers))
                minimum = map_node.children[0].leafs[0]
                if not res.t:
                    res = minimum 
                if res.cost > minimum.cost:
                    res = minimum

    #generate new tree from the best position from next piece 2
    if depth == 2:
        for l1 in root.leafs[:3]:
            for l2 in l1.children[0].leafs[:2]:
                for map_node in l2.children[0].leafs[:1]:

                    map_node.add_child(generate_base_tree(piece_type, map_node.data, cost_multipliers))
                    minimum = map_node.children[0].leafs[0]
                    if not res.t:
                        res = minimum 
                    if res.cost > minimum.cost:
                        res = minimum

    if not res.t:
        res = None
    return res
        
                       


#returns insert location, assuming list is sorted
def insert(elem, lista):
	if lista == []:
		return 0
	if elem.cost > lista[0].cost:
		return 1 + insert(elem, lista[1:])
	return insert(elem, lista[1:])
