from django.urls import path
from .views import ObtainJSONWebToken, RefreshJSONWebToken, RegistrationAPIView, LoginAPIView, BookDetailView, PageDetailView

urlpatterns = [
    path('api/token/', ObtainJSONWebToken.as_view(), name='obtain_token'),
    path('api/token/refresh/', RefreshJSONWebToken.as_view(), name='refresh_token'),
    path('api/registration/', RegistrationAPIView.as_view(), name='registration'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/books/<int:book_id>/', BookDetailView.as_view(), name='book_detail'),
    path('api/pages/<int:page_id>/', PageDetailView.as_view(), name='page_detail'),
]

