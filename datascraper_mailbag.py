import email
import imaplib
from email.header import decode_header
from msal import PublicClientApplication

# THIS DOES NOT WORK YET. will need help from the Ethans figuring out API client permissions nonsense.

app = PublicClientApplication(
    "msal36581a01-b5e7-44ac-b969-6404d081bff2",
    authority="https://login.microsoftonline.com/common"
)
result = app.acquire_token_interactive(scopes=["User.Read"])
if "access_token" in result:
    print(result["access_token"])  # Yay!
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))
# account credentials
user = "csc131-team03@csussandbox.onmicrosoft.com"
passw = "VFR$5tgbVFR$5tgb**"
#imap_server = "outlook.office365.com"

def clean(text):

    return "".join(c if c.isalnum() else "_" for c in text)


# IMAP4 class and authentication
#imap = imaplib.IMAP4_SSL(imap_server)
#imap.login(user,passw)

N = 3
