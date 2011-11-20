import gtk
from generator_task import GeneratorTask


class Gui(gtk.Window):
    
    def __init__(self, engine):
        super(Gui, self).__init__()
        
        self.error = False
        
        self.set_size_request(290, 52)
        self.set_border_width(10)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("kung-fy")
        self.connect("destroy", gtk.main_quit)
        
        vb = gtk.VBox()
        self.add(vb)
        self.progress_bar = gtk.ProgressBar()
        vb.pack_start(self.progress_bar)
        
#        self.textfield = gtk.Label()
#        self.textfield.set_text("defaulttext")
#        self.add(self.textfield)
        
        self.engine = engine
        self.thread_task = GeneratorTask(engine.prepare, self.on_progress, self.on_prepare_done)
        self.thread_task.start()
        self.show_all()
        
    def on_progress(self, success, message):
        if success:
            self.progress_bar.set_text(message)
            self.progress_bar.pulse()
        else:
            self.error = True
            self.message = message
        
    def on_prepare_done(self):
        if self.error:
            self.show_error_message(self.message)
            self.thread_task.exit()
        else:
            self.thread_task = GeneratorTask(self.engine.run_player, self.on_progress, self.on_player_closed)
            self.hide_all()
            self.thread_task.start()
        
    def on_player_closed(self):
        self.show_all()
        if self.error:
            self.show_error_message(self.message)
            self.thread_task.exit()
        else:
            self.thread_task = GeneratorTask(self.engine.wrap_up, self.on_progress, self.on_wrapup_done)
            self.thread_task.start()
        
    def on_wrapup_done(self):
        if self.error:
            self.show_error_message(self.message)
            self.thread_task.exit()
        gtk.main_quit()
        
    def show_info_message(self, message):
        md = gtk.MessageDialog(self,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()
    
    def show_error_message(self, message):
        md = gtk.MessageDialog(self,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
            gtk.BUTTONS_CLOSE, message)
        md.run()
        md.destroy()


