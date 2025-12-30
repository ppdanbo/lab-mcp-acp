from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base as prompt_base


mcp = FastMCP() 

@mcp.prompt(title="Attention Prompt", description="A prompt is used to get the user to pay attention to a message.")
async def show_prompt(message: str) -> str:
    return f"Please pay attention to message: {message}"

@mcp.prompt(title="Debug Code", description="A prompt to help debug code snippets.")
async def debug_code(code: str) -> list[prompt_base.Message]:
    return [
        prompt_base.UserMessage("I can see this code has errors"),
        prompt_base.AssistantMessage("What has you tried so far?"),
    ]
    