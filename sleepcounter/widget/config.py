_updates_per_min = 120

def set_update_rate(rate: int):
    """Sets the widget update rate in updates per minute"""
    _updates_per_min = rate

def get_update_rate():
    """Returns the widget update rate in updates per minute"""
    return _updates_per_min