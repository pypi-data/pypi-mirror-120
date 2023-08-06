from logging import debug
from mupemenet.mvc.utils.Utils import delta_s
from timeit import default_timer as timer

from mupemenet.osdependent.PlatformDependentTripleClickListener import PlatformDependentTripleClickListener


class RpiTripleClickListener(PlatformDependentTripleClickListener):

    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.click_timestamp = 0

    def enter(self, params=None):
        self.register_triple_click_event(params)
        

    def exit(self):
        pass

    def register_triple_click_event(self, params):

        widget, root, (w, h) = params

        def toogle_fullscreen(event):
            if delta_s(self.click_timestamp)<3:
                return
            debug("Toggleling Fullscreen mode")
            if (root.attributes('-fullscreen')):
                root.attributes('-fullscreen', False)
                root.geometry(f'{w//2}x{h//2}')
            else:
                root.attributes('-fullscreen', True) 

        def handle_triple_click(event):
  
            if self.click_timestamp == 0:
                self.click_timestamp = timer()
                self.click_count = 1
                return
            ts = timer()
            delta = ts - self.click_timestamp

            if delta <= 0.35:
                self.click_count += 1
                self.click_timestamp = ts

            elif self.click_count == 3:
                self.click_count = 0
                self.click_timestamp = 0

            elif delta > 0.35:
                self.click_count = 1
                self.click_timestamp = ts

            debug("Clicked!!!. Delta: {}. Clicks: {}".format(delta, self.click_count))
            if self.click_count == 3:
                RpiTripleClickListener.triple_button_click_action(None)
        
        widget.bind("<Button-1>", handle_triple_click)
        widget.bind("<ButtonRelease-1>", toogle_fullscreen)
