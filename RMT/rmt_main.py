import os

import yaml

import modules.action as action
import modules.deparser as deparser
import modules.match as match
import modules.match_crossbar as match_crossbar
import modules.parser as parser
import modules.payload_store as payload_store
import modules.queue as queue
import simulator.read_args as read_args

def main():
    
    '''
    Main simulator for the RMT pipeline.

    The RMT simulator uses a tick based model.
    '''

    # 1) Set up simulator
    args = read_args.read_args()
    config = yaml.safe_load(open(args.config_path, "r"))
    pkt_files = get_pkt_files(config["input_pkts_path"])
    time = 0

    # 2a) Set up ingress pipeline
    in_parser = parser.Parser()
    in_payload_store = payload_store.Payload_Store()
    in_xbar1 = match_crossbar.Match_Crossbar(["src_ip", "dst_ip"])
    in_match1 = match.Match([[1, {'src_ip': '10.0.0.3', 
                                        'dst_ip': '10.0.0.4'},
                                    [("SET", "10.0.0.5", None, None, "dst_ip"),
                                     ("SET", "1", None, None, "egress_port_m")]]])
    in_action1 = action.Action()
    in_deparser = deparser.Deparser(config["data_buffer_path"])

    # 2b) Set up queue
    sw_queue = queue.Queue(["1","2","3"])

    # 2c) Set up egress pipeline
    out_parser = parser.Parser()
    out_payload_store = payload_store.Payload_Store()
    out_xbar1 = match_crossbar.Match_Crossbar(["ttl"])
    out_match1 = match.Match([[1, {'ttl':'10'}, [("SET","9",None,None,"ttl")]],
                              [1, {'ttl':'6'}, [("SET","5",None,None,"ttl")]],
                              [1, {'ttl':'5'}, [("SET","4",None,None,"ttl")]]])
    out_action1 = action.Action()
    out_deparser = deparser.Deparser(config["output_pkts_path"])
    
    
    # 3) Run simulator until there are no more packets to process
    for pkt_file in pkt_files:

        # 3a) Ingress pipeline
        in_parser.tick(pkt_file)
        in_parser.update_registers()

        in_payload_store.store_payload(in_parser.get_payload())

        in_xbar1.tick(in_parser.get_pkt())
        in_xbar1.update_registers()

        in_match1.tick(in_xbar1.get_pkt_subset())
        in_match1.update_registers()

        in_action1.tick(in_parser.get_pkt(), 
                        in_match1.get_action_set())
        in_action1.update_registers()

        in_deparser.tick(in_action1.get_pkt(),
                         in_payload_store.get_payload(in_action1.get_pkt()))
        in_deparser.update_registers()

        # 3b) Queues
        sw_queue.tick(in_deparser.get_port(), in_deparser.get_handle(), time)
        sw_queue.update_registers()

        # 3c) Egress pipeline
        out_parser.tick(sw_queue.get_pkt())
        out_parser.update_registers()

        out_payload_store.store_payload(out_parser.get_payload())

        out_xbar1.tick(out_parser.get_pkt())
        out_xbar1.update_registers()

        out_match1.tick(out_xbar1.get_pkt_subset())
        out_match1.update_registers()

        out_action1.tick(out_parser.get_pkt(), 
                        out_match1.get_action_set())
        out_action1.update_registers()

        out_deparser.tick(out_action1.get_pkt(),
                          out_payload_store.get_payload(out_action1.get_pkt()))
        out_deparser.update_registers()

        break

            

def get_pkt_files(path):

    '''
    Returns a list of the files in the folder that contains packets.
    '''

    filenames = [fn for fn in os.listdir(path) if ".xml" in fn]
    filepaths = [os.path.join(path, fn) for fn in filenames]
    return filepaths

if __name__ == "__main__":
    main()
