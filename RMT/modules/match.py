import copy

class Match:

    '''
    Simulates an RMT match table.

    Has a set of rules, where each rule is a (pri, match, action_set) tuple.
    Match consists of a dictionary mapping match fields to the rule's value.
    An action_set is a tuple of actions.
    An action is a tuple: (OP, OPERAND_1, OPERAND_2, OPERAND_3, OUT_FIELD)

    On tick, takes a packet subset and checks to see if the subset is equal
    to any of its rules' match fields. If it is, sets that rule's action set
    to self.action_set. If it isn't raise Exception.
    '''

    def __init__(self, rules):

        # Match rule indices
        self.PRI = 0
        self.MATCH = 1
        self.ACTION = 2
        
        self.rules = rules

        self.action_set = None
        self.action_set_r = None


    def tick(self, pkt_subset):
        
        hi_pri, action_set = -float('inf'), None
        for r in self.rules:
            if r[self.MATCH] == pkt_subset and r[self.PRI] > hi_pri:
                hi_pri, action_set = r[self.PRI], r[self.ACTION]

        if action_set == None:
            raise Exception(("Could not find match "
                             "for pkt_subset:{}").format(pkt_subset))
        
        self.action_set = action_set
        
    def update_registers(self):
        self.action_set_r = copy.deepcopy(self.action_set)

    def get_action_set(self):
        return self.action_set_r

    
                         

                            
        
