import os
import sys
import re
import random
import string
import requests
from requests.auth import HTTPDigestAuth

from ONVIFMessage import ONVIFMessage

args = {}
known_payloads = []


def analyse_response(req, param, payload, rsp, exception):
    """
    Analyse the response rsp from the server against the payload in req
    :param req: Request string containing the payload
    :param param: The fuzzed parameter
    :param payload: The payload used
    :param rsp: Optional Response object
    :param exception: Optional Exception object
    :return: None
    """
    if rsp is None:  # Exception during request, server crash ?
        if type(exception) is requests.exceptions.ConnectionError:
            print('Server crashes:')
            print(req.decode('ascii'))
            print(exception)
        else:
            print('Exception during request:')
            print(req.decode('ascii'))
            print(exception)
    else:  # Server response, analyse return code
        if 400 <= rsp.status_code < 500:  # HTTP code to indicate client error, server detects error: fine
            print('Client error detected by the server:')
        elif rsp.status_code >= 500:  # HTTP code to indicate server error, service crash ?
            print('Server error:')
        else:  # HTTP code to indicate that request was accepted, good ?
            print('Request accepted by the server:')

        print(req.decode('ascii'))
        print(rsp.content.decode('ascii'))


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
        message.set_param(p, message.params[p].default)


def generate_payloads(n_random=100):
    """
    Generate pseudo random payloads from regex from parameter type, totally random string and known payloads
    :param n_random: Number of random payloads
    :return: An array of strings containing payloads
    """
    global known_payloads

    # x = Xeger(limit=50)

    # Pseudo random payloads
    # payloads = [x.xeger(ParamTypes[type_param]['regex']) for i in range(n_pseudo)]

    payloads = []

    # Random payloads
    for i in range(n_random):
        payloads.append(''.join(
            random.choice(string.ascii_letters + string.digits + string.punctuation + string.whitespace)
            for j in range(random.randint(5, 50))))

    # Buffer overflow payloads
    payloads.append('A' * 1025)
    payloads.append('A' * 2049)
    payloads.append('A' * 4097)
    payloads.append('A' * 8193)

    # Known payloads
    for p in known_payloads:
        payloads.append(p)

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

    payloads = generate_payloads(args['count'])

    for payload in payloads:
        message.set_param(param, payload)
        req = message.get_message()
        rsp = None
        exception = None

        try:
            rsp = requests.post('http://{host}:{port}{url}'.format(host=args['host'], port=args['port'],
                                                                   url=args['url']),
                                req, auth=HTTPDigestAuth(args['user'], args['password']), timeout=30)  # timeout based on ONVIF Device Test Tool
            exception = None
        except Exception as e:
            rsp = None
            exception = e
        finally:
            analyse_response(req, param, payload, rsp, exception)


if __name__ == "__main__":
    def usage():
        sys.stderr.write('Usage: {} <template file> <ip address> [-p <port>] <service url> <user> <password> '
                         '<known payloads file> <payload count per parameter>\n'.format(sys.argv[0]))
        sys.exit(1)

    def validate_file(arg):
        if not os.path.exists(arg):
            sys.stderr.write("{} doesn't exist\n".format(arg))
            usage()
        else:
            return arg

    def validate_host(arg):
        r = re.compile('[0-9]{1,3}')
        numbers = r.findall(arg)
        if len(numbers) != 4 or int(numbers[0]) == 0 or \
                any([True if int(n) < 0 or int(n) > 255 else False for n in numbers]):
            sys.stderr.write('Invalid IP address\n')
            usage()
        return arg

    def validate_port(arg):
        if not arg.isdecimal():
            sys.stderr.write('Port must be a number\n')
            usage()
        if int(arg) > 65535 or int(arg) == 0:
            sys.stderr.write('Port must be a number between 1 and 65535\n')
            usage()
        return int(arg)

    def validate_service_url(arg):
        if arg == '':
            usage()
        return arg

    if len(sys.argv) != 8 and len(sys.argv) != 10:
        usage()

    args['template'] = validate_file(sys.argv.pop(1))
    args['host'] = validate_host(sys.argv.pop(1))
    if sys.argv[1] == '-p':
        sys.argv.pop(1)
        args['port'] = validate_port(sys.argv.pop(1))
    else:
        args['port'] = 80
    args['url'] = validate_service_url(sys.argv.pop(1))
    args['user'] = sys.argv.pop(1)
    args['password'] = sys.argv.pop(1)
    load_known_payloads(validate_file(sys.argv.pop(1)))
    try:
        args['count'] = int(sys.argv.pop(1))
        if args['count'] < 0:
            sys.stderr.write('Count must be a positive number')
            usage()
    except:
        sys.stderr.write('Count must be a number')
        usage()

    message = ONVIFMessage(args['template'])
    for param in message.get_all_params():
        fuzz_param(message, param)
