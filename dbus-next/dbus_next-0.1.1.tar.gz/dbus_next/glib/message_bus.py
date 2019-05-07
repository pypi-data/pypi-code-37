from __future__ import annotations

from .._private.unmarshaller import Unmarshaller
from ..constants import BusType
from ..message import Message
from ..constants import MessageType, MessageFlag, NameFlag, RequestNameReply, ReleaseNameReply
from ..message_bus import BaseMessageBus
from .._private.auth import auth_external, auth_begin, auth_parse_line, AuthResponse
from ..errors import AuthError
from .proxy_object import ProxyObject
from .. import introspection as intr

import logging
import io
from typing import Callable, Optional

# glib is optional
_import_error = None
try:
    from gi.repository import GLib
    _GLibSource = GLib.Source
except ImportError as e:
    _import_error = e

    class _GLibSource:
        pass


class _MessageSource(_GLibSource):
    def __init__(self, bus):
        self.unmarshaller = None
        self.bus = bus

    def prepare(self):
        return (False, -1)

    def check(self):
        return False

    def dispatch(self, callback, user_data):
        try:
            while self.bus._stream.readable():
                if not self.unmarshaller:
                    self.unmarshaller = Unmarshaller(self.bus._stream)

                if self.unmarshaller.unmarshall():
                    callback(self.unmarshaller.message)
                    self.unmarshaller = None
                else:
                    break
        except Exception as e:
            self.bus.disconnect()
            self.bus._finalize(e)
            return GLib.SOURCE_REMOVE

        return GLib.SOURCE_CONTINUE


class _MessageWritableSource(_GLibSource):
    def __init__(self, bus):
        self.bus = bus
        self.buf = b''
        self.message_stream = None
        self.chunk_size = 128

    def prepare(self):
        return (False, -1)

    def check(self):
        return False

    def dispatch(self, callback, user_data):
        try:
            if self.buf:
                self.bus._stream.write(self.buf)
                self.buf = b''

            if self.message_stream:
                while True:
                    self.buf = self.message_stream.read(self.chunk_size)
                    if self.buf == b'':
                        break
                    self.bus._stream.write(self.buf)
                    if len(self.buf) < self.chunk_size:
                        self.buf = b''
                        break
                    self.buf = b''

            self.bus._stream.flush()

            if not self.bus._buffered_messages:
                return GLib.SOURCE_REMOVE
            else:
                message = self.bus._buffered_messages.pop(0)
                self.message_stream = io.BytesIO(message._marshall())
                return GLib.SOURCE_CONTINUE
        except BlockingIOError:
            return GLib.SOURCE_CONTINUE
        except Exception as e:
            self.bus._finalize(e)
            return GLib.SOURCE_REMOVE


class _AuthLineSource(_GLibSource):
    def __init__(self, stream):
        self.stream = stream
        self.buf = b''

    def prepare(self):
        return (False, -1)

    def check(self):
        return False

    def dispatch(self, callback, user_data):
        self.buf += self.stream.read()
        if self.buf[-2:] == b'\r\n':
            callback(self.buf)
            return GLib.SOURCE_REMOVE

        return GLib.SOURCE_CONTINUE


class MessageBus(BaseMessageBus):
    """The message bus implementation for use with the GLib main loop.

    The message bus class is the entry point into all the features of the
    library. It sets up a connection to the DBus daemon and exposes an
    interface to send and receive messages and expose services.

    You must call :func:`connect() <dbus_next.glib.MessageBus.connect>` or
    :func:`connect_sync() <dbus_next.glib.MessageBus.connect_sync>` before
    using this message bus.

    :param bus_type: The type of bus to connect to. Affects the search path for
        the bus address.
    :type bus_type: :class:`BusType <dbus_next.BusType>`
    :param bus_address: A specific bus address to connect to. Should not be
        used under normal circumstances.

    :ivar unique_name: The unique name of the message bus connection. It will
        be :class:`None` until the message bus connects.
    :vartype unique_name: str
    """

    def __init__(self, bus_address: str = None, bus_type: BusType = BusType.SESSION):
        if _import_error:
            raise _import_error

        super().__init__(bus_address, bus_type, ProxyObject)
        self._main_context = GLib.main_context_default()

    def connect(self, connect_notify: Callable[[MessageBus, Optional[Exception]], None] = None):
        """Connect this message bus to the DBus daemon.

        This method or the synchronous version must be called before the
        message bus can be used.

        :param connect_notify: A callback that will be called with this message
            bus. May return an :class:`Exception` on connection errors or
            :class:`AuthError <dbus_next.AuthError>` on authorization errors.
        :type callback: :class:`Callable`
        """
        self._stream.write(b'\0')
        self._stream.write(auth_external())
        self._stream.flush()

        def on_authline(line):
            response, args = auth_parse_line(line)

            if response != AuthResponse.OK:
                raise AuthError(f'authorization failed: {response.value}: {args}')

            self._stream.write(auth_begin())
            self._stream.flush()

            self.message_source = _MessageSource(self)
            self.message_source.set_callback(self._on_message)
            self.message_source.attach(self._main_context)

            self.writable_source = None

            self.message_source.add_unix_fd(self._fd, GLib.IO_IN)

            def on_hello(reply, err):
                if err:
                    if connect_notify:
                        connect_notify(reply, err)
                    return

                self.unique_name = reply.body[0]

                for m in self._buffered_messages:
                    self.send(m)

                if connect_notify:
                    connect_notify(self, err)

            def on_match_added(reply, err):
                if err:
                    logging.error(f'adding match to "NameOwnerChanged" failed: {err}')
                    self.disconnect()
                    return

            hello_msg = Message(destination='org.freedesktop.DBus',
                                path='/org/freedesktop/DBus',
                                interface='org.freedesktop.DBus',
                                member='Hello',
                                serial=self.next_serial())

            match = "sender='org.freedesktop.DBus',interface='org.freedesktop.DBus',path='/org/freedesktop/DBus',member='NameOwnerChanged'"
            add_match_msg = Message(destination='org.freedesktop.DBus',
                                    path='/org/freedesktop/DBus',
                                    interface='org.freedesktop.DBus',
                                    member='AddMatch',
                                    signature='s',
                                    body=[match],
                                    serial=self.next_serial())

            self._method_return_handlers[hello_msg.serial] = on_hello
            self._method_return_handlers[add_match_msg.serial] = on_match_added
            self._stream.write(hello_msg._marshall())
            self._stream.write(add_match_msg._marshall())
            self._stream.flush()

        self._auth_readline(on_authline)

    def connect_sync(self) -> MessageBus:
        """Connect this message bus to the DBus daemon.

        This method or the asynchronous version must be called before the
        message bus can be used.

        :returns: This message bus for convenience.
        :rtype: :class:`MessageBus <dbus_next.glib.MessageBus>`

        :raises:
            - :class:`AuthError <dbus_next.AuthError>` - If authorization to \
              the DBus daemon failed.
            - :class:`Exception` - If there was a connection error.
        """
        main = GLib.MainLoop()
        connection_error = None

        def connect_notify(bus, err):
            nonlocal connection_error
            connection_error = err
            main.quit()

        self.connect(connect_notify)
        main.run()

        if connection_error:
            raise connection_error

        return self

    def call(self,
             msg: Message,
             reply_notify: Callable[[Optional[Message], Optional[Exception]], None] = None):
        """Send a method call and asynchronously wait for a reply from the DBus
        daemon.

        :param msg: The method call message to send.
        :type msg: :class:`Message <dbus_next.Message>`
        :param reply_notify: A callback that will be called with the reply to
            this message. May return an :class:`Exception` on connection errors.
        :type reply_notify: Callable
        """
        self._call(msg, reply_notify)

    def call_sync(self, msg: Message) -> Optional[Message]:
        """Send a method call and synchronously wait for a reply from the DBus
        daemon.

        :param msg: The method call message to send.
        :type msg: :class:`Message <dbus_next.Message>`

        :returns: A message in reply to the message sent. If the message does
            not expect a reply based on the message flags or type, returns
            ``None`` immediately.
        :rtype: :class:`Message <dbus_next.Message>`

        :raises:
            - :class:`DBusError <dbus_next.DBusError>` - If the service threw \
                  an error for the method call or returned an invalid result.
            - :class:`Exception` - If a connection error occurred.
        """
        if msg.flags & MessageFlag.NO_REPLY_EXPECTED or msg.message_type is not MessageType.METHOD_CALL:
            self.send(msg)
            return None

        if not msg.serial:
            msg.serial = self.next_serial()

        main = GLib.MainLoop()
        handler_reply = None
        connection_error = None

        def reply_handler(reply, err):
            nonlocal handler_reply
            nonlocal connection_error

            handler_reply = reply
            connection_error = err

            main.quit()

        self._method_return_handlers[msg.serial] = reply_handler
        self.send(msg)
        main.run()

        if connection_error:
            raise connection_error

        return handler_reply

    def introspect_sync(self, bus_name: str, path: str) -> intr.Node:
        """Get introspection data for the node at the given path from the given
        bus name.

        Calls the standard ``org.freedesktop.DBus.Introspectable.Introspect``
        on the bus for the path.

        :param bus_name: The name to introspect.
        :type bus_name: str
        :param path: The path to introspect.
        :type path: str

        :returns: The introspection data for the name at the path.
        :rtype: :class:`Node <dbus_next.introspection.Node>`

        :raises:
            - :class:`InvalidObjectPathError <dbus_next.InvalidObjectPathError>` \
                    - If the given object path is not valid.
            - :class:`InvalidBusNameError <dbus_next.InvalidBusNameError>` - If \
                  the given bus name is not valid.
            - :class:`DBusError <dbus_next.DBusError>` - If the service threw \
                  an error for the method call or returned an invalid result.
            - :class:`Exception` - If a connection error occurred.
        """
        main = GLib.MainLoop()
        request_result = None
        request_error = None

        def reply_notify(result, err):
            nonlocal request_result
            nonlocal request_error

            request_result = result
            request_error = err

            main.quit()

        super().introspect(bus_name, path, reply_notify)
        main.run()

        if request_error:
            raise request_error

        return request_result

    def request_name_sync(self, name: str, flags: NameFlag = NameFlag.NONE) -> RequestNameReply:
        """Request that this message bus owns the given name.

        :param name: The name to request.
        :type name: str
        :param flags: Name flags that affect the behavior of the name request.
        :type flags: :class:`NameFlag <dbus_next.NameFlag>`

        :returns: The reply to the name request.
        :rtype: :class:`RequestNameReply <dbus_next.RequestNameReply>`

        :raises:
            - :class:`InvalidBusNameError <dbus_next.InvalidBusNameError>` - If \
                  the given bus name is not valid.
            - :class:`DBusError <dbus_next.DBusError>` - If the service threw \
                  an error for the method call or returned an invalid result.
            - :class:`Exception` - If a connection error occurred.
        """
        main = GLib.MainLoop()
        request_result = None
        request_error = None

        def reply_notify(result, err):
            nonlocal request_result
            nonlocal request_error

            request_result = result
            request_error = err

            main.quit()

        super().request_name(name, flags, reply_notify)
        main.run()

        if request_error:
            raise request_error

        return request_result

    def release_name_sync(self, name: str) -> ReleaseNameReply:
        """Request that this message bus release the given name.

        :param name: The name to release.
        :type name: str

        :returns: The reply to the release request.
        :rtype: :class:`ReleaseNameReply <dbus_next.ReleaseNameReply>`

        :raises:
            - :class:`InvalidBusNameError <dbus_next.InvalidBusNameError>` - If \
                  the given bus name is not valid.
            - :class:`DBusError <dbus_next.DBusError>` - If the service threw \
                  an error for the method call or returned an invalid result.
            - :class:`Exception` - If a connection error occurred.
        """
        main = GLib.MainLoop()
        release_result = None
        release_error = None

        def reply_notify(result, err):
            nonlocal release_result
            nonlocal release_error

            release_result = result
            release_error = err

            main.quit()

        super().release_name(name, reply_notify)
        main.run()

        if release_error:
            raise release_error

        return release_result

    def send(self, msg: Message):
        if not msg.serial:
            msg.serial = self.next_serial()

        self._buffered_messages.append(msg)

        if self.unique_name:
            self._schedule_write()

    def get_proxy_object(self, bus_name: str, path: str, introspection: intr.Node) -> ProxyObject:
        return super().get_proxy_object(bus_name, path, introspection)

    def _schedule_write(self):
        if self.writable_source is None or self.writable_source.is_destroyed():
            self.writable_source = _MessageWritableSource(self)
            self.writable_source.attach(self._main_context)
            self.writable_source.add_unix_fd(self._fd, GLib.IO_OUT)

    def _auth_readline(self, callback):
        readline_source = _AuthLineSource(self._stream)
        readline_source.set_callback(callback)
        readline_source.add_unix_fd(self._fd, GLib.IO_IN)
        readline_source.attach(self._main_context)
        # make sure it doesnt get cleaned up
        self._readline_source = readline_source
