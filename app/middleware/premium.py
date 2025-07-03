from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from app.config import settings

security = HTTPBearer(auto_error=False)

async def verify_premium_access(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> bool:
    """
    Verify if the user has premium access.
    
    For now, this is a simple API key check.
    In production, this would integrate with your payment system.
    """
    if not settings.ENABLE_PREMIUM_FEATURES:
        # If premium features are disabled globally, allow access
        return True
    
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Premium feature requires authentication"
        )
    
    # Simple API key validation for demo purposes
    if credentials.credentials != settings.PREMIUM_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid premium API key or subscription required"
        )
    
    return True

def require_premium(func):
    """
    Decorator to protect premium endpoints.
    """
    async def wrapper(*args, **kwargs):
        # Extract request from args/kwargs
        request = None
        for arg in args:
            if isinstance(arg, Request):
                request = arg
                break
        
        if not request:
            raise HTTPException(
                status_code=500,
                detail="Internal error: Request object not found"
            )
        
        # Verify premium access
        await verify_premium_access(request)
        
        # Call the original function
        return await func(*args, **kwargs)
    
    return wrapper

class PremiumFeature:
    """
    Context manager for premium feature checks.
    """
    def __init__(self, feature_name: str):
        self.feature_name = feature_name
    
    async def __aenter__(self):
        if not settings.ENABLE_PREMIUM_FEATURES:
            return self
        
        # Add any premium feature specific logic here
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
