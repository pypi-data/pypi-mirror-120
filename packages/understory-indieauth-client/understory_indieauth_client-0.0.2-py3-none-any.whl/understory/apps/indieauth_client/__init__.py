"""An IndieAuth client for the Understory framework."""

from indieauth import client
from understory import web
from understory.web import tx

__all__ = ["app"]

app = web.application(
    __name__,
    prefix="access",
    model=client.model.schemas,
)


def wrap(handler, mainapp):
    """Ensure client database contains users table."""
    # TODO store User Agent and IP address with `sessions`
    # TODO attach session to this user
    tx.auth_client = client.model(tx.db)
    yield


@app.control(r"")
class Users:
    """Site users."""

    def get(self):
        """Return a list of users to owner, the current user or a sign-in page."""
        if tx.user.session:
            if tx.user.is_owner:
                return app.view.users(tx.auth_client.get_users())
            else:
                return tx.user.session
        else:
            return app.view.signin(tx.host.name)


@app.control(r"sign-in")
class SignIn:
    """IndieAuth client sign in."""

    def get(self):
        """Initiate a sign-in."""
        form = web.form("me", return_to="/")
        tx.user.session["return_to"] = form.return_to
        raise web.SeeOther(client.initiate_sign_in(tx.origin, form.me))


@app.control(r"authorize")
class Authorize:
    """IndieAuth client authorization redirect URL."""

    def get(self):
        """Complete a sign-in by requesting a token."""
        form = web.form("state", "code")
        response = client.authorize_sign_in(form.state, form.code, "profile")
        tx.user.session["uid"] = response["me"]
        raise web.SeeOther(tx.user.session["return_to"])


@app.control(r"sign-out")
class SignOut:
    """IndieAuth client sign out."""

    def get(self):
        """Return a sign-out form."""
        return app.view.signout()

    def post(self):
        """Sign the user out."""
        form = web.form(return_to="/")
        client.sign_out(tx.user.session["uid"])
        tx.user.session = None
        raise web.SeeOther(form.return_to)
