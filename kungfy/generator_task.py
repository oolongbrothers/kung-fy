'''
@author: Ali Afshar, see http://unpythonic.blogspot.com/2007/08/using-threads-in-pygtk.html
'''

import threading, thread
import gobject, gtk

gtk.gdk.threads_init() #@UndefinedVariable


class GeneratorTask(object):

    def __init__(self, generator, loop_callback, complete_callback=None):
        self.generator = generator
        self.loop_callback = loop_callback
        self.complete_callback = complete_callback
    
    def _start(self, *args, **kwargs):
        self._stopped = False
        for ret in self.generator(*args, **kwargs):
            if self._stopped:
                thread.exit()
            gobject.idle_add(self._loop, ret)
        if self.complete_callback is not None:
            gobject.idle_add(self.complete_callback)
    
    def _loop(self, ret):
        if ret is None:
            ret = ()
        if not isinstance(ret, tuple):
            ret = (ret,)
        self.loop_callback(*ret)
    
    def start(self, *args, **kwargs):
        threading.Thread(target=self._start, args=args, kwargs=kwargs).start()
    
    def stop(self):
        self._stopped = True
        
    def exit(self):
        thread.exit()

