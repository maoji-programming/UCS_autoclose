from config.loader import load

__config = load("credentials","driver","timeout","url")
if __config is None:
    raise FileNotFoundError("Configuration file not found or could not be loaded.")

def get_instance():
    """
    Get the loaded configuration instance.
    """
    global __config
    return __config