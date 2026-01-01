
import asyncio

from acp_sdk.client import Client
from acp_sdk.models import Message, MessagePart

async def example() -> None:
    async with Client(base_url="http://localhost:8000") as client:
        # run = await client.run_sync(agent="Greetings", input=Message(parts=[MessagePart(content="Danbo")]))
        # print(run.output[0].parts[0].content)
        user_msg = Message(
            role="user", 
            parts=[MessagePart(content="Entropy")]
            )
        result = await client.run_sync(
            agent="MeaningAgent", 
            input=[user_msg]
        )
        print(f"Client output: {result.output[-1].parts[0].content}")

if __name__ == "__main__":
    asyncio.run(example())
