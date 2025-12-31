from turtle import st
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel 
import asyncio
import redis    

# mcp = FastMCP(stateless_http=True)
mcp = FastMCP()


class Greeting(BaseModel):
    message: str

@mcp.tool("Greeting")
def run_greetings(name: str, ctx: Context) -> Greeting:
    """
        A tool function that accepts a parameter name and returns a personalised greeting message.
    """
    
    session_id = ctx.session_id
    print(f"Session ID: {session_id}")
    redis_client = redis.Redis(host='localhost', port=6379, username="", password="", db=0)
   
    stored_name = redis_client.get(session_id).decode('utf-8')
    if stored_name is None:
         redis_client.set(session_id, name)
     
    ctx.info("Returning result from redis: " + stored_name)  
    try:  
        stored_name = redis_client.get(session_id).decode('utf-8')
    except AttributeError:
        ctx.error("Failed to decode stored name from Redis. It may not be set yet.")
        stored_name = redis_client.get(session_id)        
    except Exception as e:
        ctx.error("Error retrieving name from redis: " + str(e))
        
    return Greeting(message=f"Hello, {stored_name}!")


# mcp.run(transport="streamable-http")
async def main():
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())