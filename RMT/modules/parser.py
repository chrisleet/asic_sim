import copy

import xmltodict

class Parser:

    '''
    Takes a handle to an XML pkt as in input, and parses it into a pkt dict.
    '''

    def __init__(self):

        # Internal data
        self.pkt = None
        self.payload = None

        # Registers
        self.pkt_r = None
        self.payload_r = None

    def tick(self, pkt_handle):

        '''
        Get header and payload from file, tag each with filename as id
        '''

        with open(pkt_handle) as f:

            full_pkt = xmltodict.parse(f.read())
            
            self.pkt = dict(full_pkt["packet"]["header"])
            self.pkt["sim_id"] = pkt_handle
            self.pkt["egress_port_m"] = 1

            self.payload = {}
            self.payload["payload"] = full_pkt["packet"]["payload"]
            self.payload["sim_id"] = pkt_handle


    def update_registers(self):
        self.pkt_r = copy.deepcopy(self.pkt)
        self.payload_r = copy.deepcopy(self.payload)
        
    def get_pkt(self):
        return self.pkt_r
    
    def get_payload(self):
        return self.payload_r
