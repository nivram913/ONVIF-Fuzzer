Files in this folder are ONVIF commands templates extracted from SoapUI 5.4.0 project file. To do so, we configure SoapUI to include type of parameters in comments. Then we create a new SOAP project with the option that generate request samples.

We used the following python program to extract command templates from the project file:
```python
import sys
import os
import xml.etree.ElementTree as etree


def get_command_name(req):
    """
    Return the command's name from a SOAP message
    :param req: String
    :return: String
    """
    root = etree.fromstring(req)
    tag_name = root.find('{http://www.w3.org/2003/05/soap-envelope}Body')[0].tag
    return tag_name[tag_name.find('}') + 1:]


if __name__ == '__main__':
    """main"""
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: {} <SOAPUI project file>'.format(sys.argv[0]))
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        sys.stderr.write("{} doesn't exist".format(sys.argv[1]))
        sys.exit(1)

    tree = etree.parse(sys.argv[1])
    root_node = tree.getroot()
    operations = root_node.find('{http://eviware.com/soapui/config}interface')\
        .findall('{http://eviware.com/soapui/config}operation')
    for op in operations:
        req = op.find('{http://eviware.com/soapui/config}call').find('{http://eviware.com/soapui/config}request').text\
            .replace('\\r', '')
        command_name = get_command_name(req)

        # Check if file exist and create an unique name
        number = 0
        while os.path.exists('{}{}.xml'.format(command_name, number)):
            number += 1

        # Write command to file
        with open('{}{}.xml'.format(command_name, number), 'w') as f:
            f.write(req)

```
