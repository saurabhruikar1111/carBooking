from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
import pytz
import datetime
from django.conf import settings

class TokenAuthenticationModified(TokenAuthentication):
    
    def authenticate_credentials(self, key):
        try:
            token=Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")
        
        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted")
        
        utc_now = datetime.datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)
        
        token_expiration_time_inseconds = settings.REST_FRAMEWORK.get("TOKEN_EXPIRATION",300)
        if token.created < utc_now - datetime.timedelta(seconds=token_expiration_time_inseconds):
            token.delete()
            raise AuthenticationFailed("Token has expired")
        
        return token.user,token