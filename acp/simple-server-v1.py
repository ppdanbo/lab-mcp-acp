from acp_sdk.server import Server
from acp_sdk.models import Message

server = Server()

@server.agent("NameAgent")
async def nameagent(messages: list[Message]) -> str:
    names = []
    for message in messages:
        print(f"message: {message}")
        for part in message.parts:
            names.append(part.content)  
    return f"Hello {', and '.join(names)}!"

server.run(port=8090)