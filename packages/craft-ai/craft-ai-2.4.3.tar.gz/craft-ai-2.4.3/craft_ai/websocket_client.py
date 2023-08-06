import websockets
import asyncio
import json
from .errors import (
    CraftAiCredentialsError,
    CraftAiBadRequestError,
    CraftAiNotFoundError,
    CraftAiUnknownError,
    CraftAiInternalError,
)


def get_error_from_websocket_status(status_code, message):
    """Give the error corresponding to the status code for websocket.

    :param int status_code: status code of the response to
    a request.
    :param str message: error message given by the response.

    :return: error corresponding to the status code.
    :rtype: Error.
    """

    if status_code == 1007:
        err = CraftAiBadRequestError(message)
    elif status_code == 1003:
        err = CraftAiNotFoundError(message)
    elif status_code == 1002:
        err = CraftAiInternalError(message)
    else:
        err = CraftAiUnknownError(message)
    return err


def initialize_websocket(url, headers):
    web_socket_event_loop = asyncio.get_event_loop()
    try:
        [protocol, uri] = url.split("://")
    except ValueError:
        raise CraftAiBadRequestError("Invalid url provided")
    ws_protocol = ("wss://", "ws://")[protocol == "http"]
    ws_url = ws_protocol + uri + "/api/ws"
    try:
        websocket = web_socket_event_loop.run_until_complete(
            websockets.connect(
                ws_url, subprotocols=["echo-protocol"], extra_headers=headers
            )
        )
    except websockets.exceptions.InvalidStatusCode as e:
        raise CraftAiCredentialsError(e)
    return websocket


def send_payload_websocket(websocket, payload):
    web_socket_event_loop = asyncio.get_event_loop()
    try:
        web_socket_event_loop.run_until_complete(websocket.send(payload))
    except websockets.exceptions.ConnectionClosedError as e:
        try:
            error_message = web_socket_event_loop.run_until_complete(websocket.recv())
        except websockets.exceptions.ConnectionClosedError as error:
            raise CraftAiUnknownError(error.reason)
        raise get_error_from_websocket_status(e.code, error_message)


def wait_for_server_response_websocket(websocket):
    web_socket_event_loop = asyncio.get_event_loop()
    try:
        # first recv is to get the error message
        # second one is to wait until the server closes the connection
        #  to have the status_code
        error_message = web_socket_event_loop.run_until_complete(websocket.recv())
        web_socket_event_loop.run_until_complete(websocket.recv())
    except websockets.exceptions.ConnectionClosedError as e:
        raise get_error_from_websocket_status(e.code, error_message)
    except websockets.exceptions.ConnectionClosedOK as e:
        result = json.loads(e.reason)
        return int(result["nbOperationsAdded"])
