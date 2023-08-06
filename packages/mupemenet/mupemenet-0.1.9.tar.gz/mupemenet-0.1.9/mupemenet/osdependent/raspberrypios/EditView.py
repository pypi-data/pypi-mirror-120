import logging as log
from tkinter import Entry
import dbus


class EditView(Entry):

    def __init__(self, *args, **kwargs) -> None:
        ui_root = kwargs.pop('ui_root')
        super(EditView, self).__init__(*args, **kwargs)

        def focus_off(event):
            ui_root.attributes('-fullscreen', True)
            log.info("Hiding keyboard")
            self.get_interface().hide()

        def focus_on(event):
            ui_root.attributes('-fullscreen', False)
            log.info("Showing keyboard")
            self.get_interface().show()

        self.bind("<Enter>", focus_on)
        self.bind("<Return>", focus_off)

    def get_interface(self):
        try:
            bus = dbus.SessionBus()
            florence = bus.get_object('org.florence.Keyboard',
                                      '/org/florence/Keyboard')
            iface = dbus.Interface(florence,
                                   dbus_interface='org.florence.Keyboard')
            print("Florence interface acquired")
        except dbus.exceptions.DBusException:
            log.error('Dbus exception occured:( Florence not started?')
        else:
            return iface
