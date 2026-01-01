from acp_sdk.server import Server
from acp_sdk.models import Message, MessagePart

from beeai_framework.backend.chat import ChatModel # only needed if Agent is using LLM
from beeai_framework.agents.react import ReActAgent
from beeai_framework.memory.token_memory import TokenMemory

import os
import dotenv
dotenv.load_dotenv()

server = Server()

@server.agent("MeaningAgent")
async def meaning(messages: list[Message]) -> str:
    """A agent function that extract text from last user message and returns its meaning."""

    user_input = messages[-1].parts[0].content  # Get the content of the last message from the user    
    #supported llm names are "ollama", "openai", "watsonx", "groq", "xai", "vertexai", "amazon_bedrock", "anthropic", "azure_openai", "mistralai"
    llm= ChatModel.from_name("openai:" + os.getenv("OPENAI_MODEL"))
    
    memory = TokenMemory(llm)
    agent = ReActAgent(llm=llm, 
                       tools=[], 
                       memory=memory)
    
    response = await agent.run(f"Find the meaning of the word: {user_input}. Be concise and return one sentence.",)
    final_answer = response.iterations[-1].state.final_answer
    print(f"\nFinal Answer: {final_answer}")
    return final_answer

server.run() 