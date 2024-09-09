from os import environ

from gui.app import app

if __name__ == "__main__":
    debug = environ.get("DEBUG", False)
    if debug:
        import debugpy
        debugpy.listen(5678)
        debugpy.wait_for_client()

    app.launch()
