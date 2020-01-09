from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from django.contrib.auth.models import User
from blog_api.serializers import UserSerializer, PostListSerializer, PostcreateSerializer, CreateUserSerializer, LoginUserSerializer
from rest_framework.views import APIView
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from rest_framework.reverse import reverse
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from tempcheck.models import Post
from rest_framework.permissions import IsAuthenticated, AllowAny
from blog_api.permissions import IsOwnerOrReadOnly
from django.db.models import Q
from blog_api.pagination import PostLimitOffPagination

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from  rest_framework.views import APIView




class UserViewset(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer


# class UserApiView(APIView):
#
#     def post(self, request):
#         print("requesting data:", request.data)
#         username = self.request.data.get('username')
#         password = self.request.data.get('password')
#         if username is not None:
#             user = User.objects.filter(username=username, password=password)
#             login(request, user=user)
#             url_redirect = reverse('temp_home')
#             print("url rediecting")
#             return HttpResponseRedirect(url_redirect)


class PostcreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostcreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostcreateSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostListApiView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostListSerializer
    pagination_class = PostLimitOffPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()
        return queryset


class PostDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    # lookup_field = 'pk'
    # lookup_url_kwarg = 'pk'


class PostDeleteApiView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CreateUserApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer


class UserLoginApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer


    def post(self, request, *args, **kwargs):
        date = request.data
        serilizer = LoginUserSerializer(data=date)
        if serilizer.is_valid(raise_exception=True):
            new_data = serilizer.data
            return Response(new_data, status=HTTP_200_OK)
        return  Response(serilizer._errors, status=HTTP_400_BAD_REQUEST)







