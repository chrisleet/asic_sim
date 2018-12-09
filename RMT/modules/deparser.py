import os

import dicttoxml

from xml.dom.minidom import parseString


class Deparser:

    '''
    Takes a pkt header and its payload and writes it to a XML file.

    The XML file is stored in the file out_path. The filepath
    of the last deparsed packet is accessible by calling get_last_out_pkt()
    '''

    def __init__(self, out_path):
        self.out_path = out_path

        self.out_handle = None
        self.out_port = None
                
        self.out_handle_r = None
        self.out_port_r = None

    def tick(self, pkt, payload):
        
        # 1) Remove metadata and tag from packet header
        out_header = {k:v for (k,v) in pkt.items() 
                      if k != "sim_id" and not k.endswith("_m")}

        # 2) Build packet
        out_pkt = {}
        out_pkt["header"] = out_header
        out_pkt["payload"] = payload["payload"]
        
        # 3) Format packet
        xml = dicttoxml.dicttoxml(out_pkt, custom_root="packet",
                                  attr_type=False)
        dom = parseString(xml)
        out_txt = dom.toprettyxml()

        # 4) Write out packet
        out_handle = os.path.join(self.out_path, os.path.basename(pkt["sim_id"]))
        with open(out_handle, "w") as f:
            f.write(out_txt)

        # 5) Store packet handle and egress port
        self.out_handle = out_handle
        self.out_port = pkt["egress_port_m"]

    def update_registers(self):
        self.out_handle_r = self.out_handle
        self.out_port_r = self.out_port

    def get_handle(self):
        return self.out_handle_r
    
    def get_port(self):
        return self.out_port_r
