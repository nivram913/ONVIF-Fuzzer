# ONVIF Fuzzer

*Python 3.6.5*

## Requirements

- requests >= 2.18.4
- xeger >= 0.3.3

## Description

This tool is for fuzz parameters of ONVIF messages (IP cameras are targeted right now).

## Usage

```
Fuzzer.py <template file> <ip address> [-p <port>] <service url> <user> <password> <default values file> <known payloads file>
```
- Template files are included in *commands_templates* directory
- \<ip address> is the address of an IP camera
- You can specify a custom destination port with *-p* option
- The *service url* is the url that handle the ONVIF service (like "/onvif/device_service")
- You must specify *user* and *password* for authenticate requests (for now, only HTTP Digest is currently in use)
- Default values file serve to provide default value for parameters that are not fuzzed (**it is recommended to have one default values file per ONVIF command**)
- You can specify a custom known attacks list file in the last argument

### Form of the default values file
This file is a list of parameter type followed by a equal sign and the default value:
```
ParamType=value
```
A template of this file is included as *default_values_skeleton.txt*. You can specify only a subset of all parameter type.

## TODO

- Improve command line arguments handling with argparse for example to add features
- Add a better *analyse_response()* function
- In ONVIFMessage, use SoapUI comments to add or delete optional XML nodes
