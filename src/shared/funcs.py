from src.shared.imports import *

def path(relative_path: str) -> str:
    """A function to retrieve the path of a relative path; to be used when mode is in window.

    Args:
        relative_path (str): Path to the file wanting to find the real path to.

    Returns:
        str: Real path.
    """
    
    try:
        # Pyinstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    
    except AttributeError:
        # If _MEIPASS isn't found, signifying a non-exe, use the original path.
        base_path = os.path.abspath(".")
    
    # Return the relative path with the real base_path attached.
    return os.path.join(base_path, relative_path)