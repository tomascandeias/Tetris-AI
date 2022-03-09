                                    ###################
                                    ##    AI AGENT   ##
                                    ###################

from ai_agent.game_handler import *
from ai_agent.brain_tree import *

class agent:
    def __init__(self, cost_multipliers):
        self.cost_multipliers = cost_multipliers
        self.piece = None
        self.next_pieces = []
        self.tree = None
        self.goal = None
        self.state = None
        self.lowest_cost_prediction = None
        self.updating = False        
        self.check = "ok"

    
    def get_node_path(self, node):
        if not node:
            return None
        if not node.parent:
            return [node]
        return self.get_node_path(node.parent) + [node]

    def update_goal(self):
        #get map from first piece that leads to the future lowest cost map
        temp = self.get_node_path(self.lowest_cost_prediction)
        if temp:
            self.goal = temp[2]
            return "ok"
        else:
            return "error"    
    
    #get new goal    
    def brain_cycle(self, game, piece, next_pieces):
        self.updating = True
        self.piece = coords_to_piece(piece)
        self.state = coord_to_bitmap(game)
        self.next_pieces = next_pieces
        self.tree = generate_base_tree(self.piece[0], self.state, self.cost_multipliers)
        self.lowest_cost_prediction = None
        
        for p in self.next_pieces:
            
            self.lowest_cost_prediction = insert_next_piece_to_tree(self.tree, coords_to_piece(p, True)[0], self.cost_multipliers)

        
        self.check = self.update_goal()
        self.updating = False 
        

    #achieve current goal
    def move_cycle(self, piece):
        self.piece = coords_to_piece(piece)
        return get_best_key(self.goal, self.piece, self.state)




def get_best_key(best_position_node, piece, game_map):
    #rotation
    if not best_position_node.parent.data == piece[1]:
        return 'w'
    #current x_position compared to desired x_position
    simulation_piece = piece_to_bitmap(piece)
    piece_map = piece_to_bitmap(piece)
    while not (game_map|simulation_piece) == best_position_node.data:
        simulation_piece = simulation_piece << 1
    scanner = BORDER_LEFT
    current = 0
    wanted = 0
    while not scanner & simulation_piece:
        scanner = sh_r(scanner,1)
        wanted += 1
    scanner = BORDER_LEFT
    while not scanner & piece_map:
        scanner = sh_r(scanner,1)
        current += 1

    if current == wanted:
        return 's'
        #Não clicar S para isso damos o que mesmo ?? 
    if current < wanted:
        return 'd'
    if current > wanted:
        return 'a'
    return ''
