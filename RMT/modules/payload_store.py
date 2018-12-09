class Payload_Store():

    '''
    Stores each packet's payload while its header is in the parser.
    '''

    def __init__(self):
        self.store = {}

    def store_payload(self, payload):
        self.store[payload["sim_id"]] = payload

    def get_payload(self, pkt):

        if pkt["sim_id"] not in self.store.keys():
            raise Exception("ID:{} not in payload store")

        payload = self.store[pkt["sim_id"]]
        del self.store[pkt["sim_id"]]
        return payload
            
    
