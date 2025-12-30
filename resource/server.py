from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP()

class UserProfile(BaseModel):
    user_id: str
    name: str
    email: str
    
# Static resource. Is discovered by resource/list
@mcp.resource("config://app",
               name="Config",
               title="Application Configuration", 
               description="Returns application configuration settings.")
def get_config() -> dict:
    """
        A resource function that returns application configuration settings.
    """
    return {
        "app_name": "MyApp",    
    }

# Dynamic Resource. Is discovered by resources/templates/list
@mcp.resource("users://{user_id}/profile", 
              name="User Profile", 
              title="User Profile",
              description="Returns user profile information based on user_id.")
def get_user_profile(user_id: str) -> UserProfile:
    """
        A resource function that returns user profile information based on user_id.
        In a real application, this would fetch data from a database or external service

    """
    return_profile = UserProfile(user_id=user_id, name="John Doe", email="john.doe@example.com")
    return return_profile