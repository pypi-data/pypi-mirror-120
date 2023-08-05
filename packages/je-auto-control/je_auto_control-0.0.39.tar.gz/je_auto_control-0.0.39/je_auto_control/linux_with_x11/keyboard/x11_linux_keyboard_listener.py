import sys

if sys.platform not in ["linux", "linux2"]:
    raise Exception("should be only loaded on linux")

from Xlib.display import Display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq

from threading import Thread

# get current display
current_display = Display()


class KeypressHandler(Thread):

    def __init__(self, default_daemon=True):
        """
        setDaemon : default damon is true
        still listener : continue listener keycode ?
        event_key_code : now current key code default is 0
        """
        super().__init__()
        self.setDaemon(default_daemon)
        self.still_listener = True
        self.event_keycode = 0

    # two times because press and release
    def check_is_press(self, keycode):
        """
        :param keycode we want to check
        """
        if keycode == self.event_keycode:
            self.event_keycode = 0
            return True
        else:
            return False

    def run(self, reply):
        """
        :param reply listener return data
        get data
        while data not null and still listener
            get event

        """
        try:
            data = reply.data
            while len(data) and self.still_listener:
                event, data = rq.EventField(None).parse_binary_value(data, current_display.display, None, None)
                # run two times because press and release event
                self.event_keycode = event.detail
        except Exception:
            raise Exception


class XWindowsKeypressListener(Thread):

    def __init__(self, default_daemon=True):
        """
        :param default_daemon default kill when program down
        create handler
        set root
        """
        super().__init__()
        self.setDaemon(default_daemon)
        self.still_listener = True
        self.handler = KeypressHandler()
        self.root = current_display.screen().root
        self.context = None

    def check_is_press(self, keycode):
        """
        :param keycode check this keycode is press?
        """
        return self.handler.check_is_press(keycode)

    def run(self):
        """
        while still listener
            get context
            set handler
            set record
            get event
        """
        if self.still_listener:
            try:
                # Monitor keypress and button press
                if self.context is None:
                    self.context = current_display.record_create_context(
                        0,
                        [record.AllClients],
                        [{
                            'core_requests': (0, 0),
                            'core_replies': (0, 0),
                            'ext_requests': (0, 0, 0, 0),
                            'ext_replies': (0, 0, 0, 0),
                            'delivered_events': (0, 0),
                            'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
                            'errors': (0, 0),
                            'client_started': False,
                            'client_died': False,
                        }])
                    current_display.record_enable_context(self.context, self.handler.run)
                    current_display.record_free_context(self.context)
                # keep running this to get event
                next_event = self.root.display.next_event()
            except Exception:
                raise Exception
            finally:
                self.handler.still_listener = False
                self.still_listener = False


xwindows_listener = XWindowsKeypressListener()
xwindows_listener.start()


def check_key_is_press(keycode):
    """
    :param keycode check this keycode is press?
    """
    return xwindows_listener.check_is_press(keycode)

