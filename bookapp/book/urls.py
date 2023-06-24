from django.urls import path
from .views import *

urlpatterns = [
    path('api/token/', ObtainJSONWebToken.as_view(), name='obtain_token'),
    path('api/token/refresh/', RefreshJSONWebToken.as_view(), name='refresh_token'),
    path('api/registration/', RegistrationAPIView.as_view(), name='registration'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/booksList/', BookList.as_view(), name='BookList'),
    path('api/booksCreate/', BookCreate.as_view(), name='BookListCreate'),
    path('api/books/<int:book_id>/', BookDetailView.as_view(), name='BookDetailView'),
    path('api/pagesList/', PageList.as_view(), name='PageList'),
    path('api/pagesCreate/', PageCreate.as_view(), name='PageCreate'),
    path('api/pages/<int:page_id>/', PageDetailView.as_view(), name='PageDetailView'),
]

