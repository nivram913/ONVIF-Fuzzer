import sys
import os
import xml.etree.ElementTree as etree
from xml.sax.saxutils import unescape

from ONVIFMessage import ONVIFMessage

requests = {}  # Requests as XML node extracted from ONVIF Device Test Tool result file
templates = {}  # Requests as ONVIFMessage object templates read from templates files


def usage():
    sys.stderr.write('Usage: {} <ODTT results file> <templates directory> <output directory>\n'.format(sys.argv[0]))
    sys.exit(1)


def get_request_content(request):
    """
    Return the body of a POST HTTP request from a string
    If not found, return a zero length string
    :param request: HTTP request as string
    :return: String
    """
    offset = request.find('\n\n')
    return request[offset + 2:] if offset != -1 else ''


def get_request_name(envelope):
    """
    Return the ONVIF command name from an "Envelope" SOAP node
    :param envelope: Envelope SOAP XML node
    :return: String
    """
    tag = envelope.find('{http://www.w3.org/2003/05/soap-envelope}Body')[0].tag
    return tag[tag.find('}') + 1:]


def get_all_requests(name):
    """
    Search and return a list of request names from 'requests' that match the command name in parameter
    :param name: Name of an ONVIF command without a number at the end (string)
    :return: Array of string
    """
    global requests

    r = []
    for n in requests:
        # n[:-1] remove the number at the end of request name
        if name == n[:-1]:
            r.append(n)
    return r


def get_value_of(param_name, req_node):
    """
    Search and return the value of the parameter param_name in req_node hierarchy (recursive function)
    Return a zero length string if parameter is not found
    :param param_name: Parameter name
    :param req_node: Node to search from (XML node)
    :return: String
    """
    for n in req_node.getchildren():
        if n.tag[n.tag.find('}') + 1:] == param_name:
            return n.text
        r = get_value_of(param_name, n)
        if r != '':
            return r
    return ''


def map_params(req_node, template_obj):
    """
    Set all parameters of template_obj with parameters from req_node
    :param req_node: XML node
    :param template_obj: ONVIFMessage object
    :return: None
    """
    for param in template_obj.get_all_params():
        r = get_value_of(param, req_node)
        if r == '':
            continue
        template_obj.set_param(param, r)


def write(template_ojb):
    """
    Write the template_obj object to a file named with the name of the ONVIF command
    :param template_ojb: ONVIFMessage object
    :return: None
    """
    with open(sys.argv[3] + '\\' + template_ojb.name[template_ojb.name.find('}') + 1:] + '.xml', 'w') as f:
        f.write(template_ojb.get_message().decode('ascii'))


def number_of_nodes(node):
    """
    Return the number of nodes in 'node' hierarchy (recursive function)
    :param node: XML node
    :return: positive integer
    """
    if len(node.getchildren()) == 0:
        return 0
    r = len(node)
    for n in node.getchildren():
        r += number_of_nodes(n)
    return r


def correspondence(node1, node2):
    """
    Return the similitude between node1 and node2 in term of node number
    :param node1: XML node
    :param node2: XML node
    :return: positive integer
    """
    return abs(number_of_nodes(node1) - number_of_nodes(node2))


def extract_all_requests(file_path):
    """
    Populate requests global dictionary with requests extracted from ODTT result file at file_path
    :param file_path: Path to the file
    :return: None
    """
    global requests

    odtt = etree.parse(file_path)
    odtt_root = odtt.getroot()

    test_results = odtt_root.find('Results').findall('TestResult')

    for test_result in test_results:
        step_results = test_result.find('Log').find('Steps').findall('StepResult')

        for step_result in step_results:
            request = step_result.find('Request')

            if request is None:
                continue

            request_content = unescape(get_request_content(request.text))

            # If no HTTP body found
            if request_content == '':
                continue

            # Parse SOAP message contained in body
            request_root = etree.fromstring(request_content)
            request_name = get_request_name(request_root)

            # Generate an unique name by adding a number at the end
            i = 0
            while request_name + str(i) in requests:
                i += 1

            requests[request_name + str(i)] = request_root


if __name__ == '__main__':
    if len(sys.argv) != 4:
        usage()

    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("{} doesn't exist\n".format(sys.argv[1]))
        usage()

    if not os.path.isdir(sys.argv[2]):
        sys.stderr.write("{} must be a directory\n".format(sys.argv[2]))
        usage()

    if not os.path.isdir(sys.argv[3]):
        os.mkdir(sys.argv[3])

    # Construct requests sample list
    extract_all_requests(sys.argv[1])

    # Construct templates template list
    list_templates = os.listdir(sys.argv[2])
    for fic in list_templates:
        # Filter only .xml files
        if fic[-4:] != '.xml':
            continue
        templates[fic[:-4]] = ONVIFMessage(sys.argv[2] + '\\' + fic)

    # Search for commands in templates that have been executed in the test from ODTT
    # keep is a list of couple: (template name, list of corresponding request names)
    keep = []
    for template in templates:
        request_names = get_all_requests(template[:-1])
        if len(request_names) == 0:
            print('{} not executed during ONVIF Test'.format(template))
            continue

        keep.append((template, request_names))

    # For all templates and associated requests
    for template, request_names in keep:
        # Sort requests to map parameters from less similar requests first
        sorted_request_names = [(correspondence(requests[n][0], templates[template].tree.getroot()[1]), n)
                                for n in request_names]
        sorted_request_names.sort(reverse=True)

        # Initialize parameters with a zero length string to avoid '?' parameter value
        for p in templates[template].get_all_params():
            templates[template].set_param(p, '')

        # Map parameters from requests to template in previously defined order
        for rn in sorted_request_names:
            map_params(requests[rn[1]], templates[template])

        # Write the template to a file
        write(templates[template])
