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




class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Check if the object has an attribute named 'user'
        if hasattr(obj, 'user'):
            return obj.user == request.user

        # For objects without 'user' attribute, such as 'Page' model
        # Implement custom logic here based on your requirements
        # For example, allow only if the user is an admin
        return request.user.is_superuser




class BookList(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]

    
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

    def post(self, request):
        author = request.user.author
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class BookDetailView(APIView):
    # permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    permission_classes = [AllowAny]

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
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # permission_classes = [AllowAny]

    
    def get(self, request):
        try:
            page = Page.objects.get()
            serializer = PageSerializer(page , many = True)
            return Response(serializer.data)
        except Page.DoesNotExist:
            error_message = 'there is no page to display.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)


class PageCreate(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def post(self, request):
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            success_message = 'Page created successfully.'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PageDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def Retrive(self, request, page_id):
        try:
            page = Page.objects.get(id=page_id)
            serializer = PageSerializer(page)
            return Response(serializer.data)
        except Page.DoesNotExist:
            error_message = 'Page not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, page_id):
        try:
            page = Page.objects.get(id=page_id)
            serializer = PageSerializer(page, data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = 'Page updated successfully.'
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Page.DoesNotExist:
            error_message = 'Page not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, page_id):
        try:
            page = Page.objects.get(id=page_id)
            page.delete()
            success_message = 'Page deleted successfully.'
            return Response(success_message, status=status.HTTP_204_NO_CONTENT)
        except Page.DoesNotExist:
            error_message = 'Page not found.'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)
    
    