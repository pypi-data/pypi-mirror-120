from unittest.mock import MagicMock

class LauncherApiMock:

    def __init__(self):
        self.mock_delete_launcher = MagicMock()
        self.mock_get_launcher = MagicMock()
        self.mock_replace_launcher = MagicMock()

    def delete_launcher(self, *args, **kwargs):
        """
        This method mocks the original api LauncherApi.delete_launcher with MagicMock.
        """
        return self.mock_delete_launcher(self, *args, **kwargs)

    def get_launcher(self, *args, **kwargs):
        """
        This method mocks the original api LauncherApi.get_launcher with MagicMock.
        """
        return self.mock_get_launcher(self, *args, **kwargs)

    def replace_launcher(self, *args, **kwargs):
        """
        This method mocks the original api LauncherApi.replace_launcher with MagicMock.
        """
        return self.mock_replace_launcher(self, *args, **kwargs)

