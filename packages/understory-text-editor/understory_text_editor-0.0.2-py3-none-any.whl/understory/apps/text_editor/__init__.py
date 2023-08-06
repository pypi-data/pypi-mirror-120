"""A text editor Micropub client for the Understory framework."""

from micropub import client
from understory import web

app = web.application(__name__, prefix="pub/editors/text")


@app.control(r"")
class Editor:
    """The editor."""

    def get(self):
        """Return the editor."""
        return app.view.editor()
