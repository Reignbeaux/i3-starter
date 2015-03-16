from gi.repository import Gtk
import time

time.sleep(5)
win = Gtk.Window()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()