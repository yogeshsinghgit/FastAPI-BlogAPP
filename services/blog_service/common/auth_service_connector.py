from fastapi.security import OAuth2PasswordBearer

# This tells FastAPI to look for the token in the 'Authorization' header with 'Bearer' prefix
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
