from acp_sdk.server import Server
from acp_sdk.models import Message
import os


# keep on running into the error with uvicorn assert self.ssl_certfile, we have to get around with this code
import uvicorn

# Absolute paths (Windows-safe)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_FILE = os.path.join(BASE_DIR, "certs","localhost.crt")
KEY_FILE = os.path.join(BASE_DIR, "certs", "localhost.key")

print(f"Cert file path: {CERT_FILE}")
print(f"Key file path: {KEY_FILE}")
print(os.path.exists(CERT_FILE))

# Create ACP server instance
server = Server()

@server.agent("NameAgent")
async def nameagent(names: Message) -> str:
    return f"Hello, {names[0]}!"

# Get the ASGI app from ACP
app = server.app

server.run(
    # ssl_keyfile=key_file,
    # ssl_certfile=crt_file
    ssl_keyfile="./localhost.key",
    ssl_certfile="./localhost.crt"
    )

# Run uvicorn with SSL (THIS is the key)
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8443,
    ssl_certfile=CERT_FILE,
    ssl_keyfile=KEY_FILE,
)