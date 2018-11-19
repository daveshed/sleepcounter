import datetime
import unittest
from unittest.mock import Mock

from sleepcounter.controller import Controller
from sleepcounter.time.calendar import Calendar


class ControllerIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.controller = Controller(Calendar(date_library=Mock()))
        self.mock_widget = Mock()
        self.controller.register_widget(self.mock_widget)
        
    def test_controller_updates_widgets(self):
        self.controller.update_widgets()
        self.mock_widget.update.assert_called()

    def test_deregistered_widget_does_not_get_updated(self):
        self.controller.deregister_widget(self.mock_widget)
        self.controller.update_widgets()
        self.mock_widget.update.assert_not_called()
