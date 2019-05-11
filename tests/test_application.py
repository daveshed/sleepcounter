from unittest import TestCase
from unittest.mock import Mock

from sleepcounter.application import Application
from sleepcounter.time.calendar import Calendar


class ApplicationBasicTests(TestCase):

    def setUp(self):
        self.mock_widget = Mock()
        self.app = Application([self.mock_widget])
        
    def test_application_starts_widgets(self):
        self.app.start()

        self.mock_widget.start.assert_called()

    def test_appliction_stops_widgets(self):
        self.app.stop()
        self.mock_widget.stop.assert_called()
