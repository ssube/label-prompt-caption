from os import environ

from gui.app import app

demo = app

debug = environ.get("DEBUG", False)
if debug:
    import debugpy
    debugpy.listen(5678)
    debugpy.wait_for_client()

if __name__ == "__main__":
    demo.launch()
