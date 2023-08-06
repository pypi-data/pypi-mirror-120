import logging
from typing import Any, Optional

from .data_models import EndpointRequest


class LogEntry(logging.Logger):
    """Standardised logging."""
    def error(self, msg: Optional[Any] = None, *args, **kwargs):

        user_message: Optional[Any] = kwargs.pop('user_message', None)
        endpoint_request = kwargs.pop('endpoint_request', None)

        strings = []
        if user_message:
            strings.append(str(user_message))
        if msg and isinstance(msg, str):
            strings.append(f'Error details: {msg}')
        if endpoint_request and isinstance(endpoint_request, EndpointRequest):
            strings.append(f'{str(endpoint_request)}')
        super().error('\n'.join(string for string in strings), stack_info=True)

    def info(self, msg: Optional[Any] = None, *args, **kwargs):

        endpoint_request = kwargs.pop('endpoint_request', None)

        strings = []
        if msg and isinstance(msg, str):
            strings.append(str(msg))
        if endpoint_request and isinstance(endpoint_request, EndpointRequest):
            strings.append(f'{str(endpoint_request)}')
        super().info('\n'.join(string for string in strings))

    def debug(self, msg: Optional[Any] = None, *args, **kwargs):

        endpoint_request = kwargs.pop('endpoint_request', None)

        strings = []
        if msg and isinstance(msg, str):
            strings.append(str(msg))
        if endpoint_request and isinstance(endpoint_request, EndpointRequest):
            strings.append(f'{str(endpoint_request)}')
        super().debug('\n'.join(string for string in strings))

    def warning(self, msg: Optional[Any] = None, *args, **kwargs):

        endpoint_request = kwargs.pop('endpoint_request', None)

        strings = []
        if msg and isinstance(msg, str):
            strings.append(str(msg))
        if endpoint_request and isinstance(endpoint_request, EndpointRequest):
            strings.append(f'{str(endpoint_request)}')
        super().warning('\n'.join(string for string in strings))


class CustomDimensionsFilter(logging.Filter):
    """
    Add application-wide properties to AzureLogHandler records.
    Inspired by https://bargsten.org/wissen/python-logging-azure-custom-dimensions.html
    Workaround such that we are able to add 'Custom Properties' for the logs in Azure log
    """
    def __init__(self, custom_dimensions=None):
        """Create object with either input values or empty."""
        self.custom_dimensions = custom_dimensions or {}

    def filter(self, record):
        """Add the default custom_dimensions into the current log record."""
        cdim = self.custom_dimensions.copy()
        cdim.update(getattr(record, 'custom_dimensions', {}))
        record.custom_dimensions = cdim

        return True
