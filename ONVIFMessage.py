import os
import sys
import xml.etree.ElementTree as etree


class TreeBuilderWithComment(etree.TreeBuilder):
    def comment(self, data):
        self.start(etree.Comment, {})
        self.data(data)
        self.end(etree.Comment)


class CmdParam:
    """
    Class that represent a parameter with its type and XML node reference
    """
    def __init__(self, type, node):
        self.type = type
        self.node = node


class ONVIFMessage:
    """
    Class that represent an ONVIF message (SOAP)
    Attributes:
        name: Name of the command (String)
        params: Parameters of the command (Dictionary of CmdParam object)
    """
    def __init__(self, file):
        if not os.path.exists(file):
            sys.stderr.write("{} doesn't exist".format(file))
            return

        self.name = ''
        self.params = {}
        self.tree = etree.parse(file, parser=etree.XMLParser(target=TreeBuilderWithComment()))
        self.parse_message()

    def search_params(self, node):
        if len(node.getchildren()) == 0:
            return

        for i in range(len(node)):
            self.search_params(node[i])

            if node[i].text is None:
                return

            if node[i].text.startswith('type: '):
                param_name = node[i + 1].tag[node[i + 1].tag.find('}') + 1:]
                if param_name in self.params:
                    print('{} already in params list !'.format(param_name))
                self.params[param_name] = CmdParam(node[i].text[6:], node[i + 1])
            elif node[i].text.startswith('1 or more repetitions:'):
                pass
            elif node[i].text.startswith('Optional:'):
                pass
            elif node[i].text.startswith('You have a CHOICE of the next '):
                pass
            elif node[i].text.startswith('You may enter ANY elements at this point'):
                pass
            elif node[i].text.startswith('Zero or more repetitions:'):
                pass

    def parse_message(self):
        root_node = self.tree.getroot()
        command = root_node.find('{http://www.w3.org/2003/05/soap-envelope}Body')[0]
        self.name = command.tag

        self.search_params(command)

    def get_message(self):
        """
        Return a string of XML representation of the SOAP message
        :return: String
        """
        return etree.dump(self.tree)

    def get_all_params(self):
        """
        Return all available parameters
        :return: Array of string
        """
        return [k for k in self.params.keys()]

    def get_param(self, param):
        """
        Return the value of parameter
        :param param: Parameter name
        :return: Value of the parameter (string)
        """
        return self.params[param].node.text if param in self.params else ''

    def set_param(self, param, value):
        """
        Set parameter value
        :param param: Parameter name
        :param value: Value to set
        :return: None
        """
        if param not in self.params:
            return

        self.params[param].node.text = value


# test = ONVIFMessage('commands_templates\\SetMetadataConfiguration0.xml')
# test.get_message()
# print(test.get_all_params())
# test.set_param('VideoSourceToken', 'mdr')
# test.get_message()
