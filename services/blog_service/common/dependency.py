

from fastapi import Depends, HTTPException, status
# OR, if authentication is in a separate microservice:
import httpx
from common.auth_service_connector import oauth2_scheme

AUTH_SERVICE_URL = "http://127.0.0.1:8000/auth/user/me"  # Change this to your auth microservice URL

async def get_authenticated_user(token: str = Depends(oauth2_scheme)):
    """
    Calls the authentication microservice to validate the user.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL,
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication",
            )
        return response.json()  # This should return user details
    

# OR:

# from core.auth import get_current_user  # If auth is in the same service
# async def get_authenticated_user(user=Depends(get_current_user)):
#     """
#     Wrapper around `get_current_user` to centralize authentication.
#     """
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication",
#         )
#     return user


from fastapi import Depends, HTTPException, status

# Define required roles for each route
def require_role(required_roles: list):
    def role_checker(user=Depends(get_authenticated_user)):
        if user["role"] not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )
        return user
    return role_checker


