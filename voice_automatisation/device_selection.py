import sounddevice as sd

from simple_term_menu import TerminalMenu


def dialog() -> int:
    devices = sd.query_devices()
    options = repr(devices).splitlines()
    menu = TerminalMenu(options)
    return menu.show()
