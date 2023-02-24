from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import RegisterSerializer


@extend_schema(
    request=RegisterSerializer,
    responses=RegisterSerializer,
    description=" New user register endpoint.",
)
@api_view(http_method_names=["POST"])
def register_view(request: Request) -> Response:
    """
    New user register endpoint handling view.
    Parameters
    ----------
    request : Request
        rest_framework.request.Request - `django.http.request.HttpRequest`'s subclass - object with new user payload
    Returns
    -------
    _ : Response
        Register endpoint response with user data
    """
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
