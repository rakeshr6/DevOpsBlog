from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from tempcheck.models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'url']



class PostcreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content']


class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='post_detail_api_view')
    delete_url = serializers.HyperlinkedIdentityField(view_name='post_delete_api_view')
    author = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['url', 'title', 'content', 'author', 'img', 'date_posted', 'delete_url']

    def get_author(self, obj):
        return  str(obj.author.username)


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    email2 = serializers.EmailField(label='confirm email')

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'first_name', 'password']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("User already exists")
        return data

    def validate_email2(self, value):
        date = self.get_initial()
        email = date.get('email')
        email2 = value
        if email != email2:
            raise ValidationError("Email does not match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        first_name = validated_data['first_name']
        password = validated_data['password']
        user = User(username=username, email=email, first_name=first_name)
        user.set_password(password)
        user.save()
        return validated_data


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    token = serializers.CharField(allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'token']
        extra_kwargs = {'password':{'write_only':True}}


    def validate(self, data):
        user_obj = None
        username = data.get("username")
        password = data.get("password")
        user_qs = User.objects.filter(username=username).distinct()
        if user_qs.exists():
            user_obj = user_qs.first()
        else:
            raise ValidationError("username or password is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect crediential")
        data['token'] = 'TOKEN'
        return data


