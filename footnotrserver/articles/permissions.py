from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creators of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        #FIXME:Allow all operations while debugging
        return True
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:            
            return True
        
        # Write permissions are only allowed to the owner of the articles,annotations,comments,votes
        return obj.creator == request.user
    
