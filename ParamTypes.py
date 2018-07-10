ParamTypes = {
    'AbsoluteOrRelativeTimeType': {
        'regex':
            '([1-9][0-9]{0,3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9](Z|[\+-][0-2][0-9]:[0-5][0-9]))|' +
            '(P([1-9][0-9]*Y)?([1-9][0-9]*M)?([1-9][0-9]*D)?(T([1-9][0-9]*H)?([1-9][0-9]*M)?([1-9][0-9]*S)?)?)'
    },
    'anyURI': {
        'regex': '.*'
    },
    'AudioEncoding': {
        'regex': 'G711|G726|AAC'
    },
    'AutoFocusMode': {
        'regex': 'AUTO|MANUAL'
    },
    'AuxiliaryData': {
        'regex': '.{0,128}'
    },
    'BacklightCompensationMode': {
        'regex': 'OFF|ON'
    },
    'base64Binary': {
        'regex': '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
    },
    'Base64DERencodedASN1Value': {
        'regex': '(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
    },
    'boolean': {
        'regex': 'true|false'
    },
    'CapabilityCategory': {
        'regex': 'All|Analytics|Device|Events|Imaging|Media|PTZ'
    },
    'CertificateID': {
        'regex': '(_|[a-zA-Z])[a-zA-Z0-9_~,]*'
    },
    'CertificationPathID': {
        'regex': '(_|[a-zA-Z])[a-zA-Z0-9_~,]*'
    },
    'dateTime': {
        'regex': '[1-9][0-9]{0,3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9](Z|[\+-][0-2][0-9]:[0-5][0-9])'
    },
    'Decision': {
        'regex': 'Granted|Denied'
    },
    'Description': {
        'regex': '.{0,1024}'
    },
    'DiscoveryMode': {
        'regex': 'Discoverable|NonDiscoverable'
    },
    'DNAttributeType': {
        'regex': '[a-zA-Z0-9]*'
    },
    'DNAttributeValue': {
        'regex': '[a-zA-Z0-9]*'
    },
    'DNSName': {
        'regex': '[a-zA-Z0-9]*'
    },
    'Dot11Cipher': {
        'regex': 'CCMP|TKIP|Any|Extended'
    },
    'Dot11PSK': {
        'regex': '([0-9][a-fA-F]){0,32}'
    },
    'Dot11PSKPassphrase': {
        'regex': '[ -~]{8,63}'
    },
    'Dot11SecurityMode': {
        'regex': 'None|WEP|PSK|Dot1X|Extended'
    },
    'Dot11SSIDType': {
        'regex': '([0-9][a-fA-F]){1,32}'
    },
    'Dot11StationMode': {
        'regex': 'Ad-hoc|Infrastructure|Extended'
    },
    'DotDecimalOID': {
        'regex': '[0-9]+(.[0-9]+)*'
    },
    'Duplex': {
        'regex': 'Full|Half'
    },
    'duration': {
        'regex': 'P([1-9][0-9]*Y)?([1-9][0-9]*M)?([1-9][0-9]*D)?(T([1-9][0-9]*H)?([1-9][0-9]*M)?([1-9][0-9]*S)?)?'
    },
    'DynamicDNSType': {
        'regex': 'NoUpdate|ClientUpdates|ServerUpdates'
    },
    'EFlipMode': {
        'regex': 'OFF|ON|Extended'
    },
    'ExposureMode': {
        'regex': 'AUTO|MANUAL'
    },
    'ExposurePriority': {
        'regex': 'LowNoise|FrameRate'
    },
    'FactoryDefaultType': {
        'regex': 'Hard|Soft'
    },
    'float': {
        'regex': '(\+|-)?([0-9]*[.])?[0-9]+'
    },
    'H264Profile': {
        'regex': 'Baseline|Main|Extended|High'
    },
    'ImageStabilizationMode': {
        'regex': 'OFF|ON|AUTO|Extended'
    },
    'int': {
        'regex': '(\+|-)?[0-9]+'
    },
    'integer': {
        'regex': '(\+|-)?[0-9]+'
    },
    'IPAddressFilterType': {
        'regex': 'Allow|Deny'
    },
    'IPType': {
        'regex': 'IPv4|IPv6'
    },
    'IPv4Address': {
        'regex': '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
    },
    'IPv6Address': {
        'regex': '([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}'
    },
    'IPv6DHCPConfiguration': {
        'regex': 'Auto|Stateful|Stateless|Off'
    },
    'IrCutFilterMode': {
        'regex': 'ON|OFF|AUTO'
    },
    'JobToken': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'KeyID': {
        'regex': '(_|[a-zA-Z])[a-zA-Z0-9_~,]*'
    },
    'ModeOfOperation': {
        'regex': 'Idle|Active|Unknown'
    },
    'Mpeg4Profile': {
        'regex': 'SP|ASP'
    },
    'Name': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'NetworkHostType': {
        'regex': 'IPv4|IPv6|DNS'
    },
    'NetworkInterfaceConfigPriority': {
        'regex': '([12][0-9])|[0-9]|31'
    },
    'NetworkProtocolType': {
        'regex': 'HTTP|HTTPS|RTSP'
    },
    'nonNegativeInteger': {
        'regex': '(\+)?[0-9]+'
    },
    'OSDType': {
        'regex': 'Text|Image|Extended'
    },
    'ParityBit': {
        'regex': 'None|Even|Odd|Mark|Space|Extended'
    },
    'positiveInteger': {
        'regex': '(\+)?[0-9]+'
    },
    'PTZPresetTourDirection': {
        'regex': 'Forward|Backward|Extended'
    },
    'PTZPresetTourOperation': {
        'regex': 'Start|Stop|Pause|Extended'
    },
    'PTZPresetTourState': {
        'regex': 'Idle|Touring|Paused|Extended'
    },
    'QNameListType': {
        'regex': ''  # ?
    },
    'ReceiverMode': {
        'regex': 'AutoConnect|AlwaysConnect|NeverConnect|Unknown'
    },
    'RecordingJobMode': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'RecordingJobReference': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'RecordingReference': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'ReferenceToken': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'RelayIdleState': {
        'regex': 'closed|open'
    },
    'RelayLogicalState': {
        'regex': 'active|inactive'
    },
    'RelayMode': {
        'regex': 'Monostable|Bistable'
    },
    'ReverseMode': {
        'regex': 'OFF|ON|AUTO|Extended'
    },
    'RotateMode': {
        'regex': 'OFF|ON|AUTO'
    },
    'SetDateTimeType': {
        'regex': 'Manual|NTP'
    },
    'StreamType': {
        'regex': 'RTP-Unicast|RTP-Multicast'
    },
    'string': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'SystemLogType': {
        'regex': 'System|Access'
    },
    'token': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'TrackReference': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    },
    'TrackType': {
        'regex': 'Video|Audio|Metadata|Extended'
    },
    'TransportProtocol': {
        'regex': 'UDP|TCP|RTSP|HTTP'
    },
    'UserLevel': {
        'regex': 'Administrator|Operator|User|Anonymous|Extended'
    },
    'VideoEncoding': {
        'regex': 'JPEG|MPEG4|H264'
    },
    'WhiteBalanceMode': {
        'regex': 'AUTO|MANUAL'
    },
    'WideDynamicMode': {
        'regex': 'OFF|ON'
    },
    'XPathExpression': {
        'regex': '[a-zA-Z0-9 \r\n\t]{0,64}'
    }
}