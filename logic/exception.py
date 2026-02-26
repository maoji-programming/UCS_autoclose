class TicketNotFoundError(Exception):
    """Raised when a ticket is not found in the system."""
    pass

class TicketAlreadyClosedError(Exception):
    """Raised when attempting to close a ticket that is already closed."""
    pass

class SerialNumberMismatchError(Exception):
    """Raised when the provided serial number does not match the ticket's serial number."""
    pass

class TicketTypeError(Exception):
    """Raised when the ticket type is incorrect or unsupported."""
    pass

class WTPImcompleteError(Exception):
    """Raised when the WTP test is incomplete."""
    pass

