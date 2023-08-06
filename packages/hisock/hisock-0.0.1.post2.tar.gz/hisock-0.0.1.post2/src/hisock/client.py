"""
This module contains the HiSockClient, used to power the client
of HiSock, but also contains a `connect` function, to pass in
things automatically. It is strongly advised to use `connect`
over `HiSockClient`
"""

# Imports
from __future__ import annotations  # Remove when 3.10 is used by majority

import builtins  # Builtins, to convert string methods into builtins
import inspect  # Inspect, for type-hinting detection
import re
import socket
import json
import errno
import sys
import traceback

from functools import wraps
from typing import Union, Callable, Any

# Utilities
from utils import (
    make_header, _removeprefix,
    ServerNotRunning, iptup_to_str
)


class HiSockClient:
    """
    The client class for hisock.
    HiSockClient offers a higher-level version of sockets. No need to worry about headers now, yay!
    HiSockClient also utilizes decorators to receive messages, as an easy way of organizing your
    code structure (methods are provided, like :func:`recv_raw`, of course)

    :param addr: A two-element tuple, containing the IP address and the
        port number of the server wishing to connect to
        Only IPv4 currently supported
    :type addr: tuple
    :param name: Either a string or NoneType, representing the name the client
        goes by. Having a name provides an easy interface of sending
        data to a specific client and identifying clients. It is therefore
        highly recommended to pass in a name

        Pass in NoneType for no name (`connect` should handle that)
    :type name: str, optional
    :param group: Either a string or NoneType, representing the group the client
        is in. Being in a group provides an easy interface of sending
        data to multiple specific clients, and identifying multiple clients.
        It is highly recommended to provide a group for complex servers

        Pass in NoneType for no group (`connect` should handle that)
    :type group: str, optional
    :param blocking: A boolean, set to whether the client should block the loop
        while waiting for message or not.
        Default sets to True
    :type blocking: bool, optional
    :param header_len: An integer, defining the header length of every message.
        A smaller header length would mean a smaller maximum message
        length (about 10**header_len).
        The header length MUST be the same as the server connecting, or it will
        crash (hard to debug though).
        Default sets to 16 (maximum length of content: 10 quadrillion bytes)
    :type header_len: int, optional
    """

    def __init__(
            self,
            addr: tuple[str, int],
            name: Union[str, None],
            group: Union[str, None],
            blocking: bool = True,
            header_len: int = 16
    ):
        # Function storage
        self.funcs = {}

        # TLS arguments
        self.tls_arguments = {
            "tls": False  # If TLS is false, then no TLS
        }

        # Info for socket
        self.addr = addr
        self.name = name
        self.group = group
        self.header_len = header_len

        # Flags
        self._closed = False

        # Remember to update them as more rev funcs are added
        self.reserved_functions = [
            'client_connect',
            'client_disconnect'
        ]

        # TLS stuff (soon to be added)
        self.tls = self._TLS(self)
        self.tls_arguments = {
            "tls": False
        }
        self.called_update = False

        # Socket intialization
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect(self.addr)
        except ConnectionRefusedError:
            # Server not running
            raise ServerNotRunning(
                "Server is not running! Aborting..."
            ) from ConnectionRefusedError

        self.sock.setblocking(blocking)

        # Send client hello
        hello_dict = {"name": self.name, "group": self.group}
        conn_header = make_header(f"$CLTHELLO$ {json.dumps(hello_dict)}", self.header_len)

        self.sock.send(
            conn_header + f"$CLTHELLO$ {json.dumps(hello_dict)}".encode()
        )

    def __str__(self):
        return f"<HiSockClient connected to {iptup_to_str(self.addr)}>"

    class _TLS:
        """
        Base class for establishing TLS connections,
        and getting information about it

        TLS (Transport Layer Security) is a protocol, that basically is
        used on every internet connection. It establishes
        a secure connection between the client and the server, to prevent
        eavesdropping.

        While TLS usually allows clients and servers to pick what "suites"
        they have available, there is currently only one predefined suite
        to be used. Of course, as the projects gets bigger, more suites
        would be added.

        CLASS AND TLS IMPLEMENTATION NOT READY YET - DO NOT USE
        """

        def __init__(self, outer):
            self.outer = outer

        def enable(
                self,
                rsa_privkey_filepath='.privkey',
                suite="default"
        ):
            # TLS NOT ADDED CURRENTLY; NOT PRIORITY
            if not self.outer.called_update:
                self.outer.tls_arguments = {
                    "tls": True,
                    "rsa_privkey_filepath": rsa_privkey_filepath,
                    "suite": suite
                }

                dh_num_header = make_header("$DH_NUMS$", self.outer.header_len)
                self.outer.sock.send(
                    dh_num_header + b"$DH_NUMS$"
                )
                dh_info = self.outer.recv_raw()
                print("E", dh_info)

                if dh_info == b"$NOTLS$":
                    raise TypeError(
                        "Server has not enabled TLS"
                    )
            else:
                raise TypeError(
                    "TLS attempted to enable after `update` called"
                )

    def update(self):
        """
        Handles newly received messages, excluding the received messages for `wait_recv`
        This method must be called every iteration of a while loop, as to not lose valuable info.
        In some cases, it is recommended to run this in a thread, as to not block the
        program
        """
        self.called_update = True

        if not self._closed:  # Checks if client hasn't been closed with `close`
            try:
                while True:
                    # Receives header - If doesn't exist, server error
                    content_header = self.sock.recv(self.header_len)

                    if not content_header:
                        print("[SERVER] Connection forcibly closed by server, exiting...")
                        raise SystemExit
                    content = self.sock.recv(int(content_header.decode()))

                    for matching in self.funcs.keys():
                        if re.search(r"\$.+\$", matching):
                            raise ValueError(
                                "The format \"$command$\" is used for reserved functions - "
                                "Consider using a different format\n"
                                f"(Found with function \"{matching}\""
                            )

                    # Handle "reserved functions"
                    if content.startswith(b"$CLTCONN$") and 'client_connect' in self.funcs:
                        clt_content = json.loads(
                            _removeprefix(content, b"$CLTCONN$ ")
                        )
                        self.funcs['client_connect']['func'](clt_content)
                    elif content.startswith(b"$CLTDISCONN$") and 'client_disconnect' in self.funcs:
                        clt_content = json.loads(
                            _removeprefix(content, b"$CLTDISCONN$ ")
                        )
                        self.funcs['client_disconnect']['func'](clt_content)

                    for matching_cmd, func in self.funcs.items():
                        if content.startswith(matching_cmd.encode()) and \
                                matching_cmd not in self.reserved_functions:
                            parse_content = content[len(matching_cmd) + 1:]

                            # Type Hint -> Type Cast
                            if func['type_hint'] == str:
                                try:
                                    parse_content = parse_content.decode()
                                except UnicodeDecodeError as e:
                                    raise TypeError(
                                        f"Type casting from bytes to string failed "
                                        f"for function \"{func['name']}\":\n           {e}"
                                    ) from ValueError
                            elif func['type_hint'] == int:
                                try:
                                    parse_content = int(parse_content)
                                except ValueError as e:
                                    raise TypeError(
                                        f"Type casting from bytes to int "
                                        f"failed for function \"{func['name']}\":\n           {e}"
                                    ) from ValueError
                            elif func['type_hint'] == float:
                                try:
                                    parse_content = float(parse_content)
                                except ValueError as e:
                                    raise TypeError(
                                        f"Type casting from bytes to float "
                                        f"failed for function \"{func['name']}\":\n           {e}"
                                    ) from ValueError

                            # Call function
                            func['func'](parse_content)
            except IOError as e:
                # Normal, means message has ended
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK and not self._closed:
                    # Fatal Error, abort client (print exception, print log, exit python)
                    traceback.print_exception(
                        type(e), e, e.__traceback__, file=sys.stderr
                    )
                    print("\nServer Error encountered, aborting client...", file=sys.stderr)
                    self.close()

                    raise SystemExit

    class _on:
        """Decorator used to handle something when receiving command"""

        def __init__(self, outer: Any, command: str):
            # `outer` arg is for the HiSockClient instance
            # `cmd_activation` is the command... on activation (WOW)
            self.outer = outer
            self.command = command

        def __call__(self, func: Callable):
            """Adds a function that gets called when the client receives a matching command"""

            # Checks for illegal $cmd$ notation (used for reserved functions)
            if re.search(r"\$.+\$", self.command):
                raise ValueError(
                    "The format \"$command$\" is used for reserved functions - "
                    "Consider using a different format"
                )
            # Gets annotations of function
            annots = inspect.getfullargspec(func).annotations
            func_args = inspect.getfullargspec(func).args

            try:
                # Try to map first arg (client data)
                # Into type hint compliant one
                msg_annotation = annots[func_args[0]]
                if isinstance(msg_annotation, str):
                    msg_annotation = builtins.__dict__[annots[func_args[0]]]
            except KeyError:
                msg_annotation = None

            # Creates function dictionary to add to `outer.funcs`
            func_dict = {
                "func": func,
                "name": func.__name__,
                "type_hint": msg_annotation
            }
            self.outer.funcs[self.command] = func_dict

            # Returns the inner function, like a decorator
            return func

    def on(self, command: str):
        """
        A decorator that adds a function that gets called when the client
        receives a matching command

        Reserved functions are functions that get activated on
        specific events. Currently, there are 2 for HiSockClient:

        1. client_connect - Activated when a client connects to the server

        2. client_disconnect - Activated when a client disconnects from the server

        The parameters of the function depend on the command to listen.
        For example, reserved functions `client_connect` and
        `client_disconnect` gets the client's data passed in as an argument.
        All other nonreserved functions get the message passed in.

        In addition, certain type casting is available to nonreserved functions.
        That means, that, using type hints, you can automatically convert
        between needed instances. The type casting currently supports:

        1. bytes -> int (Will raise exception if bytes is not numerical)

        2. bytes -> str (Will raise exception if there's a unicode error)

        Type casting for reserved commands is scheduled to be
        implemented, and is currently being worked on.

        :param command: A string, representing the command the function should activate
            when receiving it
        :type command: str

        :return: The same function
            (The decorator just appended the function to a stack
        :rtype: function
        """
        # Passes in outer to _on decorator/class
        return self._on(self, command)

    def send(self, command: str, content: bytes):
        """
        Sends a command & content to the server, where it will be interpreted

        :param command: A string, containing the command to send
        :type command: str
        :param content: A bytes-like object, with the content/message
            to send
        :type content: bytes
        """
        # Creates header and sends to server
        if re.search(r"\$.+\$", command):
            raise TypeError(
                "Command format \"$command$\" is used for reserved functions - "
                "consider using a different command"
            )
        content_header = make_header(command.encode() + b" " + content, self.header_len)

        # Sends to server
        self.sock.send(
            content_header + command.encode() +
            b" " + content
        )

    def raw_send(self, content: bytes):
        """
        Sends a message to the server: NO COMMAND REQUIRED.
        This is preferable in some situations, where clients need to send
        multiple data over the server, without overcomplicating it with commands

        :param content: A bytes-like object, with the content/message
            to send
        :type content: bytes
        """
        # Creates header and send content to server, but no command
        if re.search(b"^\$.+\$", content):
            raise TypeError(
                "Command format \"$command$\" is used for reserved functions - "
                "consider not sending a message starting with $command$"
            )
        header = make_header(content, self.header_len)
        self.sock.send(
            header + content
        )

    def recv_raw(self):
        """
        Waits (blocks) until a message is sent, and returns that message.
        This is not recommended for content with commands attached;
        it is meant to be used alongside with :func:`HiSockServer.send_client_raw` and
        :func:`HiSockServer.send_group_raw`

        :return: A bytes-like object, containing the content/message
          the client first receives
        :rtype: bytes
        """
        # Blocks depending on your blocking settings, until message
        msg_len = int(self.sock.recv(self.header_len).decode())
        message = self.sock.recv(msg_len)

        # Returns message
        return message

    def close(self):
        """Closes the client; running `client.update()` won't do anything now"""
        # Changes _closed flag to True to prevent
        # `update` being crazy
        self._closed = True
        self.sock.close()


def connect(addr, name=None, group=None):
    """
    Creates a `HiSockClient` instance. See HiSockClient for more details

    :param addr: A two-element tuple, containing the IP address and
        the port number
    :type addr: tuple
    :param name: A string, containing the name of what the client should go by.
        This argument is optional
    :type name: str, optional
    :param group: A string, containing the "group" the client is in.
        Groups can be utilized to send specific messages to them only.
        This argument is optional
    :type: str, optional

    :return: A :class:`HiSockClient` instance
    :rtype: instance
    """
    return HiSockClient(addr, name, group)


if __name__ == "__main__":
    s = connect(('192.168.1.131', 33333), name="Sussus", group="Amogus")


    @s.on("Joe")
    def hehe(_):
        print("This message was sent from server after client connection\n"
              "(Sent to every client)")
        s.send("Sussus", b"Some random msg I guess")


    @s.on("pog")
    def eee(msg):
        print("Follow up message sent by server\n"
              "(Also sent to every client)")
        print("Message:", msg)
        # s.close()


    @s.on("client_connect")
    def please(data):
        print(f"Client {':'.join(map(str, data['ip']))} connected :)")


    @s.on("client_disconnect")
    def haha_bois(disconn_data):
        print(f"Aww man, {':'.join(map(str, disconn_data['ip']))} disconnected :(")


    @s.on("Test")
    def test(data):
        print("Group message received:", data)


    while True:
        s.update()
