from unittest.mock import MagicMock

class LaunchersApiMock:

    def __init__(self):
        self.mock_create_launcher = MagicMock()
        self.mock_list_launchers = MagicMock()

    def create_launcher(self, *args, **kwargs):
        """
        This method mocks the original api LaunchersApi.create_launcher with MagicMock.
        """
        return self.mock_create_launcher(self, *args, **kwargs)

    def list_launchers(self, *args, **kwargs):
        """
        This method mocks the original api LaunchersApi.list_launchers with MagicMock.
        """
        return self.mock_list_launchers(self, *args, **kwargs)

