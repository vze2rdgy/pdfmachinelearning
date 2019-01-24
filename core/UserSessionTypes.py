import enum

class UserSessionTypes(enum.Enum):
    """Different user session types"""
    Background = 1 # background session type
    Consumer = 2 # Client user session type (consumer)
    Publisher = 4 # Supplier user session type (publisher)



