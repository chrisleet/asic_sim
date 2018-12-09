import argparse

def read_args():

    '''
    Reads RMT simulator command line arguments.
    '''

    parser = argparse.ArgumentParser(description="RMT simulator")
    
    # Positional args
    parser.add_argument("config_path", help="path to simulator config")

    return parser.parse_args()
