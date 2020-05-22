#!/usr/bin/python3

import M3uParser
import logging
import os
from subprocess import Popen, PIPE
import gi
import json
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject, Gio
from gi.repository.GdkPixbuf import Pixbuf, InterpType

import urllib


GObject.threads_init()


vlc_process = None

def get_image_stream(url):
    pixbuf = None
    if "nochannel.png" in url:
        pixbuf = Pixbuf.new_from_file(url)
    else:
        response = urllib.request.urlopen(url)
        input_stream = Gio.MemoryInputStream.new_from_data(response.read(), None)
        pixbuf = Pixbuf.new_from_stream(input_stream, None)
    width = pixbuf.get_width()
    width_perc = (100*100)/width
    height = (pixbuf.get_height()*width_perc)/100
    pixbuf = pixbuf.scale_simple(100, height, InterpType.BILINEAR)
    return pixbuf

def parseM3U(url):
    logFile = "parser.log"
    myfile = M3uParser.M3uParser(logging)
    logging.basicConfig(filename=createAbsolutePath(logFile),level=logging.ERROR,format='%(asctime)s %(levelname)-8s %(message)s')
    myfile.downloadM3u(url, "list.m3u")
    json_file = {"channels": myfile.files}
    return json_file

#Check if the given path is an absolute path
def createAbsolutePath(path):
    if not os.path.isabs(path):
        currentDir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(currentDir, path)

    return path

def changeCursor(ctype, window):
    cursor = Gdk.Cursor.new(ctype)
    window.get_root_window().set_cursor(cursor)

class Handler:
    def __init__(self, iptv):
        super().__init__()
        self.iptv = iptv
        
    def on_main_destroy(self, *args):
        Gtk.main_quit()

    def on_search_changed(self, *args):
        text_filter = args[0].get_text()
        self.iptv.filter_data = text_filter
        self.iptv.new_filter.refilter()


    def on_btnActualizar_activate(self, widget):
        changeCursor(Gdk.CursorType.WATCH, self.iptv.window)
        GObject.idle_add(self.iptv.process_and_update)
        
    def on_select_row(self, *args):
        try:
            selection = self.get_selection()
            tree_filter, tree_iter = selection.get_selected()
        
            selected_user = tree_filter.get_value(tree_iter, 0)
            if selected_user < 1:
                raise Exception("Error in selected_user")
            url = tree_filter.get_model()[selected_user-1][3]
            if url:
                try:
                    args[1].set_from_pixbuf(get_image_stream(url))
                except:
                    args[1].set_from_pixbuf(get_image_stream("img/nochannel.png"))    
            else:
                args[1].set_from_pixbuf(get_image_stream("img/nochannel.png"))
        except:
            args[1].set_from_pixbuf(get_image_stream("img/nochannel.png"))
        

    def on_row_activated(self, row, col):
        model = self.get_model()
        text = str(model[row][0]) + ", " + model[row][1] + ", " + model[row][2] + ", " + model[row][3]
        global vlc_process
        if vlc_process:
            vlc_process.kill()
            vlc_process=None
        vlc_process = Popen(['vlc', '--audio', model[row][2]], stdout=PIPE, stderr=PIPE)
        

class IPTV:
    def __init__(self):
        self.url_list = ""
        builder = Gtk.Builder()
        builder.add_from_file("ui/main.glade")
        builder.connect_signals(Handler(self))
        self.window = builder.get_object("main")
        self.listmodel = Gtk.ListStore(int, str, str, str)
        self.new_filter = self.listmodel.filter_new()
        self.new_filter.set_visible_func(self.filter_model)
        self.filter_data = ""
        self.view = Gtk.TreeView.new_with_model(model=self.new_filter)
        self.logoImage = builder.get_object("logoImg")
        try:
            self.logoImage.set_from_pixbuf(get_image_stream("img/nochannel.png"))
        except Exception as ex:
            pass
        epgview = builder.get_object("epg_label")
        epgview.set_property('editable', False)

        self.epg_label = builder.get_object("epgBuffer")
        self.epg_label.set_text("EPG: Funcionalidad aun por implementar, en futuras versiones aparecera aqui la EPG")
        # cellrenderer for the first column
        cell = Gtk.CellRendererText()
        # the first column is created
        col = Gtk.TreeViewColumn("Ch num", cell, text=0)
        # and it is appended to the treeview
        self.view.append_column(col)
        cell = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn("Title", cell, text=1)
        self.view.append_column(col)

        # when a row of the treeview is selected, it emits a signal
        self.view.connect("row-activated", Handler.on_row_activated)
        self.view.connect("button-release-event", Handler.on_select_row, self.logoImage)
        scrolledWindow = builder.get_object("scrolledWindow")
        scrolledWindow.add(self.view)

        self.window.show_all()

    def fill_liststore(self):
        i=1
        self.listmodel.clear()
        for channel in self.myfile["channels"]:
            self.listmodel.append([i,channel["title"], channel["link"], channel["tvg-logo"]])
            i=i+1

    def process_and_update(self):
        self.myfile = parseM3U(self.url_list)
        self.fill_liststore()
        changeCursor(Gdk.CursorType.ARROW, self.window)

    def filter_model(self, model, iter, data):
        if not self.filter_data:
            return True
        else:
            return self.filter_data.lower() in model[iter][1].lower()
        

if __name__ == "__main__":
    iptv = IPTV()
    iptv.url_list = ""#SET YOUR IPTV LIST
    #iptv.parser_and_updete()
    Gtk.main()
