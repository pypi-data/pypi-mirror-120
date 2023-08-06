"""An IndieAuth client."""

from understory import sql, web
from understory.web import tx, uri

from .util import generate_challenge

model = sql.model(
    __name__,
    users={
        "url": "TEXT",
        "name": "TEXT",
        "email": "TEXT",
        "access_token": "TEXT",
        "account_created": "DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP",
    },
)


def initiate_sign_in(client: uri, user: uri) -> uri:
    """
    Return the URI to initiate an IndieAuth sign-in at `site` for `user`.

    `site` should be the actual sign-in endpoint URI (different for each service)
    `user` should be the identity URI for the user attempting sign in

    """
    auth = web.discover_link(user, "authorization_endpoint")
    tx.user.session["authorization_endpoint"] = str(auth)
    tx.user.session["token_endpoint"] = str(web.discover_link(user, "token_endpoint"))
    tx.user.session["micropub_endpoint"] = str(web.discover_link(user, "micropub"))
    client = uri(client)
    auth["me"] = user
    auth["client_id"] = tx.user.session["client_id"] = client
    auth["redirect_uri"] = tx.user.session["redirect_uri"] = client / "access/authorize"
    auth["response_type"] = "code"
    auth["state"] = tx.user.session["state"] = web.nbrandom(16)
    code_verifier = tx.user.session["code_verifier"] = web.nbrandom(64)
    auth["code_challenge"] = generate_challenge(code_verifier)
    auth["code_challenge_method"] = "S256"
    auth["scope"] = "create draft update delete profile email"
    return auth


def authorize_sign_in(state, code, flow):
    """Complete the authorization and return the response."""
    if state != tx.user.session["state"]:
        raise web.BadRequest("bad state")
    if flow == "profile":
        endpoint = tx.user.session["authorization_endpoint"]
    elif flow == "token":
        endpoint = tx.user.session["token_endpoint"]
    else:
        raise web.BadRequest("only `profile` and `token` flows supported")
    response = web.post(
        endpoint,
        headers={"Accept": "application/json"},
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": tx.user.session["client_id"],
            "redirect_uri": tx.user.session["redirect_uri"],
            "code_verifier": tx.user.session["code_verifier"],
        },
    ).json
    tx.auth_client.create_user(response)
    return response


def sign_out(me: uri):
    """Sign the user out by revoking the token."""
    access_token = tx.auth_client.get_user(me)["access_token"]
    web.post(
        tx.user.session["token_endpoint"],
        data={"action": "revoke", "token": access_token},
    )


@model.control
def get_users(db):
    """Return a list of users."""
    return db.select("users")


@model.control
def create_user(db, response):
    """Add a user based upon given response."""
    profile = response.get("profile", {})
    db.insert(
        "users",
        url=response["me"],
        name=profile.get("name"),
        email=profile.get("email"),
        access_token=response.get("access_token"),
    )


@model.control
def get_user(db, user: uri):
    """Return a user."""
    return db.select("users", where="url = ?", vals=[user])[0]


# @model.migrate(1)
# def change_name(db):
#     """Rename `url` to `me` to reuse language from the spec."""
#     db.rename_column("users", "url", "me")
