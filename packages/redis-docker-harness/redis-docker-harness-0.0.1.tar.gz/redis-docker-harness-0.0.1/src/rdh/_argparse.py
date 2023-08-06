import argparse


def create_parser(description, prog=None, prefix=""):
    """
    Configures a command-line parser with parameters for redis.

    :param description: the description that the parser outputs on the help screen
    :type description: str
    :param prog: the program name, when using entry_points, None to ignore
    :type prog: str
    :param prefix: the prefix to use for the command-line arguments
    :type prefix: str
    :return: the configured parser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(description=description,
                                     prog=prog,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--%shost' % prefix, metavar='HOST', required=False, default="localhost",
                        dest='redis_host', help='The redis server to connect to')
    parser.add_argument('--%sport' % prefix, metavar='PORT', required=False, default=6379, type=int,
                        dest='redis_port', help='The port the redis server is listening on')
    parser.add_argument('--%sdb' % prefix, metavar='DB', required=False, default=0, type=int,
                        dest='redis_db', help='The redis database to use')
    parser.add_argument('--%sin' % prefix, metavar='CHANNEL', required=True, type=str,
                        dest='redis_in', help='The redis channel to receive the data from')
    parser.add_argument('--%sout' % prefix, metavar='CHANNEL', required=True, type=str,
                        dest='redis_out', help='The redis channel to publish the processed data on')
    return parser
