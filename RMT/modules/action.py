import copy

# Action indexes
OPCODE = 0
OPR1 = 1
OPR2 = 2
OPR3 = 3
OUTFIELD = 4

class Action:

    '''
    Simulates an RMT action unit.
    
    Takes an action set and a pkt, and performs actions on pkt.
    
    NOTE: metadata fields must have the suffix _m
    '''

    def __init__(self):
        
        self.pkt = None
        self.pkt_r = None
          
          
    def tick(self, pkt, action_set):

        '''
        Behavior is undefined if actions in action_set conflict.
        '''
        out_pkt = copy.deepcopy(pkt)
        
        for action in action_set:
            
            if action[OPCODE] == "SET":
                set(action, out_pkt)

        self.pkt = out_pkt

    def update_registers(self):
        self.pkt_r = copy.deepcopy(self.pkt)

    def get_pkt(self):
        return self.pkt_r

def set(action, pkt):
    
    '''
    Peforms the set action on pkt.
    '''

    if isinstance(action[OPR1], int) or isinstance(action[OPR1], float):
        pkt[action[OUTFIELD]] = action[OPR1]
    elif isinstance(action[OPR1], str) and action[OPR1] in pkt.keys():
        pkt[action[OUTFIELD]] = pkt[action[[OPR1]]]
    elif isinstance(action[OPR1], str) and action[OPR1] not in pkt.keys():
        pkt[action[OUTFIELD]] = action[OPR1]
    else:
        raise Exception("Set action operand 1 type not recognized")

    
