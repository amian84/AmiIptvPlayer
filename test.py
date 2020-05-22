import time
from gi.repository import Gdk, Gtk, GObject


class MainWindow(Gtk.Window):
    """Example window."""

    def __init__(self):
        """Create new instance."""
        super(MainWindow, self).__init__()
        self.set_title('Test Windows')

        box = Gtk.VBox()
        label = Gtk.Label("Just a label....")
        box.pack_start(label, True, True, 0)
        button = Gtk.Button(" and a button")
        box.pack_start(button, True, True, 0)

        self.add(box)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    def set_watch(self):
        """Set the mouse to be a watch."""
        watch = Gdk.Cursor(Gdk.CursorType.WATCH)
        gdk_window = self.get_root_window()
        gdk_window.set_cursor(watch)

    def long_call(self):
        """Perform a long call."""
        time.sleep(10)             # your time consuming operation here
        arrow = Gdk.Cursor(Gdk.CursorType.ARROW)
        gdk_window = self.get_root_window()
        gdk_window.set_cursor(arrow)


window = MainWindow()
window.set_watch()
GObject.idle_add(window.long_call)
Gtk.main()