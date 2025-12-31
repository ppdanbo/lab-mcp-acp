from mcp.server.fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_http_headers

from pydantic import BaseModel 
import asyncio
import httpx
import os
import dotenv
from authlib.jose import JsonWebKey, JsonWebToken, JWTClaims

dotenv.load_dotenv()

mcp = FastMCP()

class Greeting(BaseModel):
    message: str

# Config for Auth2.0 Provider
OAUTH2_PROVIDER_URL = os.getenv("OAUTH2_PROVIDER_URL")  # Issuer URL 
JWKS_URI = os.getenv("JWKS_URI")  # JWKS endpoint 
AUDIENCE_URL = os.getenv("AUDIENCE_URL") # API identifier - # JWKS endpoint 

async def get_public_key(kid: str):
    """ Fetch the public key from the JWKS endpoint based on the key ID (kid) """

    async with httpx.AsyncClient() as client:
        response = await client.get(JWKS_URI)
        response.raise_for_status()
        keys = response.json()["keys"]
        for key in keys:
            return key       
        raise ValueError(f"No public key found for kid: {kid}")

@mcp.tool("Greeting")
def run_greetings(name: str) -> Greeting:
    """
        A tool function that accepts a parameter name and returns a personalised greeting message.
    """
    
    headers = get_http_headers()
    authorization_header = headers.get("Authorization")
    if authorization_header and authorization_header.startswith("Bearer "):
        try:
            token = authorization_header.replace("Bearer ", "", 1)        
            # Decode JWT to get kid 
            token_obj = JsonWebToken(algorithms=['RS256'])
            header = token_obj.decode(token, key=None, do_verify=False).header        
            kid = header.get("kid")    # kid : Key ID from token header
            if not kid:
                raise ValueError("No 'kid' found in token header")  
            
            # Fetch public key and validate token
            public_key_dict = asyncio.run(get_public_key(kid))
            public_key = JsonWebKey.import_key(public_key_dict)

            # Validate token claims
            claims: JWTClaims = token_obj.decode(token, key=public_key)
            claims.validate(iss=OAUTH2_PROVIDER_URL, aud=AUDIENCE_URL, require_scopes=None)
            token_name = claims.get("sub", "unknown")
            print("Token subject:", token)
            print("Kid:", kid)
            print("Claims:", claims)
            # Token is valid, proceed with the tool logic
        except Exception as e:
            print("Token validation failed:", str(e))
            raise ValueError("Invalid token")
    else:
        print("No valid authorization header found.")
        raise ValueError("Authorization header missing or malformed")
    
    return Greeting(message=f"Hello, {name}!")


async def main():
    await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())