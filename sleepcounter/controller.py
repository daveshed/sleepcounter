class Controller:
    
    def __init__(self, calendar):
        self._widgets = []
        self.calendar = calendar

    def update_widgets(self):
        for widget in self._widgets:
            widget.update(self.calendar)

    def register_widget(self, widget):
        self._widgets.append(widget)

    def deregister_widget(self, widget):
        self._widgets.remove(widget)