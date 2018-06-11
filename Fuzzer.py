import os
import sys
import re
import requests
from requests.auth import HTTPDigestAuth
from ParamTypes import ParamTypes
from xeger import Xeger

from ONVIFMessage import ONVIFMessage

args = {}
known_payloads = []


def analyse_response(rsp):
    """

    :param rsp:
    :return:
    """
    print(rsp.content.decode('ascii'))


def load_default_values(file):
    """
    Load default parameter value in ParamTypes from the file in the form:
    <type>=<default value>
    :param file: File containing default value
    :return: None
    """
    with open(file, 'r') as f:
        for line in f.readlines():
            type, value = line.split('=')
            ParamTypes[type]['default'] = value


def load_known_payloads(file):
    """
    Load known payloads in known_payloads string array from the file
    :param file: File containing known payloads (one per line)
    :return: None
    """
    global known_payloads

    with open(file, 'r') as f:
        known_payloads = f.readlines()


def init_all_params(message):
    """
    Initialize all parameters of message with a default value
    :param message: ONVIFMessage class
    :return: None
    """
    for p in message.get_all_params():
        message.set_param(p, ParamTypes[message.params[p].type]['default'][0])


def generate_payloads(type_param, n_pseudo=20, n_random=20):
    """
    Generate pseudo random payloads from regex from parameter type, totally random string and known payloads
    :param type_param: Type of parameter
    :param n_pseudo: Number of pseudo random payloads
    :param n_random: Number of random payloads
    :return: An array of strings containing payloads
    """
    global known_payloads

    x = Xeger(limit=50)

    # Pseudo random payloads
    payloads = [x.xeger(ParamTypes[type_param]['regex']) for i in range(n_pseudo)]

    # Known payloads
    payloads.append(known_payloads)

    return payloads


def fuzz_param(message, param):
    """
    Fuzz ONVIF message on parameter 'param'
    :param message: ONVIFMessage class
    :param param: Parameter to fuzz
    :return: None
    """
    global args

    init_all_params(message)

    payloads = generate_payloads(message.params[param].type)

    for payload in payloads:
        message.set_param(param, payload)
        rsp = requests.post('http://{host}:{port}{url}'.format(host=args['host'], port=args['port'], url=args['url']),
                            message.get_message(), auth=HTTPDigestAuth(args['user'], args['password']))
        analyse_response(rsp)


if __name__ == "__main__":
    def usage():
        sys.stderr.write('Usage: {} <template file> <ip address> [-p <port>] <service url> <user> <password> '
                         '<default values file> <known payloads file>'.format(sys.argv[0]))
        sys.exit(1)

    def validate_file(arg):
        if not os.path.exists(arg):
            sys.stderr.write("{} doesn't exist".format(arg))
            usage()
        else:
            return arg

    def validate_host(arg):
        r = re.compile('[0-9]{1,3}')
        numbers = r.findall(arg)
        if len(numbers) != 4 or int(numbers[0]) == 0 or \
                any([True if int(n) < 0 or int(n) > 255 else False for n in numbers]):
            sys.stderr.write('Invalid IP address')
            usage()
        return arg

    def validate_port(arg):
        if not arg.isdecimal():
            sys.stderr.write('Port must be a number')
            usage()
        if int(arg) > 65535 or int(arg) == 0:
            sys.stderr.write('Port must be a number between 1 and 65535')
            usage()
        return int(arg)

    def validate_service_url(arg):
        if arg == '':
            usage()
        return arg

    if len(sys.argv) != 8 and len(sys.argv) != 9:
        usage()

    args['template'] = validate_file(sys.argv.pop(1))
    args['host'] = validate_host(sys.argv.pop(1))
    if sys.argv[1] == '-p':
        args['port'] = validate_port(sys.argv.pop(1))
    else:
        args['port'] = 80
    args['url'] = validate_service_url(sys.argv.pop(1))
    args['user'] = sys.argv.pop(1)
    args['password'] = sys.argv.pop(1)
    load_default_values(validate_file(sys.argv.pop(1)))
    load_known_payloads(validate_file(sys.argv.pop(1)))

    message = ONVIFMessage(args['template'])
    for param in message.get_all_params():
        fuzz_param(message, param)
