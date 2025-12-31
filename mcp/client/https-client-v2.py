import asyncio
from urllib import response
import os
import dotenv
import httpx

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from fastmcp.client.auth import BearerAuth # type: ignore

dotenv.load_dotenv()

# from mcp.client.stdio import stdio_client

async def get_bearer_token(client_id: str, client_secret: str, token_endpoint: str, scopes: list[str] = None) -> str:
    """ Implementation for fetching the bearer token from OAuth2.0 provider """
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": os.getenv("AUDIENCE_URL"),
        }
        # if scopes:
        #     data["scope"] = " ".join(scopes)
        
        response = await client.post(
            token_endpoint, 
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
        response.raise_for_status()
        token_data = response.json()
        return token_data["access_token"]
    
async def main():

    # Google OAuth2.0 provider Details
    
    client_id = os.getenv("CLIENT_ID")
    client_secret =os.getenv("CLIENT_SECRET")    
    token_endpoint = os.getenv("TOKEN_ENDPOINT")
    scopes = None
    token = await get_bearer_token(client_id, client_secret, token_endpoint, scopes)
    
    async with streamablehttp_client(
        "http://localhost:8000/mcp",
         auth=BearerAuth(token)
        ) as ( read_stream, write_stream, _ ): 
            async with ClientSession(
                read_stream,
                write_stream                   
            ) as session:
                await session.initialize()                 
                tool_result = await session.call_tool(
                        'Greeting',
                        arguments={"name": "Alice"}                  
                    )
                print(f"\nTool call result: {tool_result}")
                greeting = tool_result.structuredContent # other result types are EmbeddedContent, RawContent and ImageContent
                print("Greetings", greeting)

        
if __name__ == "__main__":
    asyncio.run(main())

