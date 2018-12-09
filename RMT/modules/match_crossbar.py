import copy

class Match_Crossbar:

    '''
    Selects the fields in "vars" from a pkt header dict
    '''

    def __init__(self, vars):

        self.vars = vars
        self.pkt_subset = None
        self.pkt_subset_r = None

    def tick(self, pkt):

        self.pkt_subset = {k:v for (k,v) in pkt.items() if k in self.vars}

    def update_registers(self):
        self.pkt_subset_r = copy.deepcopy(self.pkt_subset)

    def get_pkt_subset(self):
        return self.pkt_subset_r
        
