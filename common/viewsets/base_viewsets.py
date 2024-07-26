from typing import Any
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from ..basepermission import IsVerified

class BaseModelviwSet(ModelViewSet):

    permission_classes = [IsAuthenticated, IsVerified]
        
        
    
    