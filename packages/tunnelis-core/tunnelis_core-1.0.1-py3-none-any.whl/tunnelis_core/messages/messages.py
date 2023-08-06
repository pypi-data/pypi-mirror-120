from enum import Enum


class MessageType(Enum):
    MSG_AUTHENTICATION_REQUEST = 1
    MSG_AUTHENTICATION_RESPONSE = 2
    MSG_OPEN_TUNNEL_REQUEST = 3
    MSG_OPEN_TUNNEL_RESPONSE = 4
    MSG_PING = 5
    MSG_PONG = 6
    MSG_RAW_REQUEST = 7
    MSG_RAW_RESPONSE = 8


class AuthenticationRequestMessage:
    type = MessageType.MSG_AUTHENTICATION_REQUEST

    def __init__(self, user, authtoken):
        self.user = user
        self.authtoken = authtoken


class AuthenticationResponseMessage:
    type = MessageType.MSG_AUTHENTICATION_RESPONSE

    def __init__(self, session_token, success=True, reason=''):
        self.session_token = session_token
        self.success = success
        self.reason = reason


class OpenTunnelRequestMessage:
    type = MessageType.MSG_OPEN_TUNNEL_REQUEST

    def __init__(self, session_token):
        self.session_token = session_token


class OpenTunnelResponseMessage:
    type = MessageType.MSG_OPEN_TUNNEL_RESPONSE

    def __init__(self, http_url, https_url, tcp_host, tcp_port, success=True, reason=''):
        self.http_url = http_url
        self.https_url = https_url
        self.tcp_host = tcp_host
        self.tcp_port = tcp_port
        self.success = success
        self.reason = reason


class PingMessage:
    type = MessageType.MSG_PING


class PongMessage:
    type = MessageType.MSG_PONG

    def __init__(self, session_token, timestamp):
        self.session_token = session_token
        self.timestamp = timestamp


class RawRequestMessage:
    type = MessageType.MSG_RAW_REQUEST

    def __init__(self, source_id, payload):
        self.source_id = source_id
        self.payload = payload


class RawResponseMessage:
    type = MessageType.MSG_RAW_RESPONSE

    def __init__(self, session_token, destination_id, payload):
        self.session_token = session_token
        self.destination_id = destination_id
        self.payload = payload
