# Indicies of (pkt, time) tuple
PKT_I = 0
TIM_I = 1


class Queue:

    '''
    Queue between ingress and egress pipelines in RMT simulator.

    Contains a queue for each egress port in the simulated switch.
    Stores a pointer each packet in the queues with the time that
    the packet entered the queue as a tuple (pkt, time). 

    The dequeueing algorithm used is modular and is given as 
    self.dequeue_f in __init__. self.dequeue_f() takes no arguments 
    and returns the tuple (egress_port, pkt).
    '''

    def __init__(self, ports):

        # 1) Generate a queue for every egress port in the switch
        self.queues = {port:[] for port in ports}

        # 2) Set dequeue function
        self.dequeue_f = self.pop_FIFO

        # 3) Dequeued pkt handle and its egress port
        self.out_port = None
        self.out_pkt = None

        self.out_port_r = None
        self.out_pkt_r = None

    def tick(self, in_port, in_pkt, time):
        
        # 1) Store new pkt in queue
        self.put(in_port, in_pkt, time)
        
        # 2) Retrieve out_pkt and out_port
        self.out_port, self.out_pkt = self.dequeue_f()

    def update_registers(self):
        self.out_port_r = self.out_port
        self.out_pkt_r = self.out_pkt

    def get_port(self):
        return self.out_port_r
    
    def get_pkt(self):
        return self.out_pkt_r
    

    ################################################
    # Some useful queue functions for rest of code #
    ################################################

    def put(self, port, v, time):
        
        '''
        Puts value v in the queue associated with port port at time time.

        Stores value v and its time as tuple (pkt, time).
        '''
        
        if port in self.queues.keys():
            self.queues[port].append((v, time))
        else:
            raise Exception("Port:{} not in queue's ports".format(port))
                                                                     

    def pop_FIFO(self):

        '''
        Gets the packet at the front of any queue with the lowest time
        '''
        
        # 1) Find the port whose queue's first pkt has the lowest time
        out_port, min_t = None, float('inf')
        for port, v in self.queues.items():
            if len(v) > 0 and v[0][TIM_I] < min_t:
                out_port, min_t = port, v[0][TIM_I]

        # 2) If no queue has length > 0, return None
        if out_port == None:
            return (None, None)
        # 3) Otherwise, remove that pkt from its port's queue. Return the
        # pkt and its port
        tmp = self.queues[out_port][0][PKT_I]
        self.queues[out_port] = self.queues[out_port][1:]
        return (out_port, tmp)
                
        

    
