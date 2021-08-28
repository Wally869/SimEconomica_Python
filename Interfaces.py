

class IClearable(object):
    """
        Interface related to clearing data in between rounds, and resetting elements
    """
    def ClearStateData(self, **kwargs):
        pass

    def ClearTempData(self):
        pass