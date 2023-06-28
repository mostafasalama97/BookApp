from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .serializers import ObtainJSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission , AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status

from .models import *
from .serializers import *
# View for obtaining JWT token
class ObtainJSONWebToken(APIView):
    serializer_class = ObtainJSONWebTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = serializer.validated_data['user']
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({'token': token})

# View for refreshing JWT token
class RefreshJSONWebToken(APIView):
    serializer_class = RefreshJSONWebTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = serializer.validated_data['payload']
        token = jwt_encode_handler(payload)

        return Response({'token': token})
    



# class IsAuthorOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         return request.user.is_authenticated
    
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         if hasattr(obj, 'user'):
#             return obj.user == request.user
#         return request.user.is_superuser


from rest_framework.permissions import BasePermission

class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS', 'POST', 'PUT', 'DELETE']:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        if request.user.is_authenticated and hasattr(obj, 'user'):
            return obj.user == request.user
        return False

class RegistrationAPIView(CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class BookList(APIView):
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    permission_classes = [AllowAny]

    
    def get(self, request):
        try:
            book = Book.objects.all()
            serializer = BookSerializer(book , many = True)
            return Response(serializer.data)
        except Book.DoesNotExist:
            error_message = 'there is no book to display.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)


class BookCreate(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAuthorOrReadOnly]

    def post(self, request):
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            author = request.user.author

            if not author:
                error_message = 'User does not have the "author" attribute.'
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(author=author)
            success_message = 'Book created successfully.'
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthorOrReadOnly]


    def get(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            error_message = 'Book not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = 'Book updated successfully.'
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            error_message = 'Book not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            success_message = 'Book deleted successfully.'
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            error_message = 'Book not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
    
    





class PageList(APIView):
       # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    permission_classes = [AllowAny]

    
    def get(self, request):
        try:
            Page = Page.objects.all()
            serializer = PageSerializer(Page , many = True)
            return Response(serializer.data)
        except Page.DoesNotExist:
            error_message = 'there is no Page to display.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)


class PageCreate(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]
    # permission_classes = [IsAuthorOrReadOnly]

    def post(self, request):
        serializer = PageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            author = request.user.author

            if not author:
                error_message = 'User does not have the "author" attribute.'
                return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(author=author)
            success_message = 'Page created successfully.'
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageDetailView(APIView):
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]
    permission_classes = [IsAuthorOrReadOnly]


    def get(self, request, Page_id):
        try:
            Page = Page.objects.get(id=Page_id)
            serializer = PageSerializer(Page)
            return Response(serializer.data)
        except Page.DoesNotExist:
            error_message = 'Page not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, Page_id):
        try:
            Page = Page.objects.get(id=Page_id)
            serializer = PageSerializer(Page, data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = 'Page updated successfully.'
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Page.DoesNotExist:
            error_message = 'Page not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, Page_id):
        try:
            Page = Page.objects.get(id=Page_id)
            Page.delete()
            success_message = 'Page deleted successfully.'
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Page.DoesNotExist:
            error_message = 'Page not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    