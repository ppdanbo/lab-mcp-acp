from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel 

mcp = FastMCP()


class Greeting(BaseModel):
    message: str

@mcp.tool("Greeting")
def run_greetings(name: str) -> Greeting:
    """
        A tool function that accepts a parameter name and returns a personalised greeting message.
    """
    return Greeting(message=f"Hello, {name}!")

mcp.run(transport="streamable-http")
