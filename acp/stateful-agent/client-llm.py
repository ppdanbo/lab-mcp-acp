import asyncio

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

async def example() -> None:
    async with Client(base_url="http://localhost:9000") as client:
        run = await client.run_sync(agent="ACP_Greetings", input=Message(parts=[MessagePart(content="Danbo")]))  
        
        print(f"Client status: {run.status}")   
        print(f"run :{run.output}")
        print(f"Client output: {run.output[0].parts[0].content}")
        

if __name__ == "__main__":
    asyncio.run(example())