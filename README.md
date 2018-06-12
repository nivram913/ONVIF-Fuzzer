# ONVIF Fuzzer

*Python 3.6.5*

## Requirements

- requests >= 2.18.4
- xeger >= 0.3.3

## Description

This tool is for fuzz parameters of ONVIF messages (IP cameras are targeted right now).

## Usage

```
Fuzzer.py <template file> <ip address> [-p <port>] <service url> <user> <password> <known payloads file>
```
- Template files are included in *commands_templates* directory
- \<ip address> is the address of an IP camera
- You can specify a custom destination port with *-p* option
- The *service url* is the url that handle the ONVIF service (like "/onvif/device_service")
- You must specify *user* and *password* for authenticate requests (for now, only HTTP Digest is currently in use)
- You can specify a custom known attacks list file in the last argument

### Default parameters value in template files

You must specify default parameters value to use in template files by replacing the '?' by its value. A tool will be released soon to use ONVIF Device Test Tool results file to populate template files.

## TODO

- Improve command line arguments handling with argparse for example to add features
- Add a better *analyse_response()* function
- In ONVIFMessage, use SoapUI comments to add or delete optional XML nodes
