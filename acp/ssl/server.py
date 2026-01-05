from acp_sdk.server import Server
from acp_sdk.models import Message
import os

# Absolute paths 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
crt_file = os.path.join(BASE_DIR, "certs", "localhost.crt")
key_file = os.path.join(BASE_DIR, "certs", "localhost.key")
print(os.path.exists(crt_file))

# Create ACP server instance
server = Server()

@server.agent("NameAgent")
async def nameagent(names: Message) -> str:
    return f"Hello, {names[0]}!"

server.run(
    ssl_keyfile=key_file,
    ssl_certfile=crt_file   
    )