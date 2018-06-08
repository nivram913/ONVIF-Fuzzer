import os
import sys
import re
import requests
from requests.auth import HTTPDigestAuth
from ParamTypes import ParamTypes

from ONVIFMessage import ONVIFMessage

args = {}


def analyse_response(rsp):
    """

    :param rsp:
    :return:
    """
    print(rsp.content.decode('ascii'))


def init_all_params(message):
    """
    Initialize all parameters of message with a default value
    :param message: ONVIFMessage class
    :return: None
    """
    for p in message.get_all_params():
        message.set_param(p, ParamTypes[message.params[p].type]['legal_values'][0])


def fuzz_param(message, param):
    """
    Fuzz ONVIF message on parameter 'param'
    :param message: ONVIFMessage class
    :param param: Parameter to fuzz
    :return: None
    """
    global args

    init_all_params(message)

    payloads = []

    for payload in payloads:
        message.set_param(param, payload)
        rsp = requests.post('http://{host}:{port}{url}'.format(host=args['host'], port=args['port'], url=args['url']),
                            message.get_message(), auth=HTTPDigestAuth('admin', 'Aveiro35'))
        analyse_response(rsp)


if __name__ == "__main__":
    def usage():
        sys.stderr.write('Usage: {} <template file> <ip address> [-p <port>] <service url>'.format(sys.argv[0]))
        sys.exit(1)

    def validate_template_file(arg):
        if not os.path.exists(arg):
            sys.stderr.write("{} doesn't exist".format(sys.argv[1]))
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

    if len(sys.argv) != 4 and len(sys.argv) != 5:
        usage()

    args['template'] = validate_template_file(sys.argv.pop(1))
    args['host'] = validate_host(sys.argv.pop(1))
    if sys.argv[1] == '-p':
        args['port'] = validate_port(sys.argv.pop(1))
    else:
        args['port'] = 80
    args['url'] = validate_service_url(sys.argv.pop(1))

    message = ONVIFMessage(args['template'])
    for param in message.get_all_params():
        fuzz_param(message, param)
