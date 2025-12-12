from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from .models import Tlitt, Comment, Hashtag, Like, Follow
from .serializers import TlittSerializer, CommentSerializer, HashtagSerializer, LikeSerializer, FollowSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied





@api_view(['POST'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)

    return Response(
        {"message": "Zarejestrowano poprawnie", "token": token.key},status=status.HTTP_201_CREATED
    )




#tłity----------------------------------------------------

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tlitt_list(request):
    if request.method == 'GET':
        tlitts = Tlitt.objects.all()
        serializer = TlittSerializer(tlitts, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tlitt_create(request):
    if request.method == 'POST':
        serializer = TlittSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def tlitt_detail(request, pk):

    try:
        tlitt = Tlitt.objects.get(pk=pk)
    except Tlitt.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not (
        request.user == tlitt.creator
        or request.user.has_perm("tlitts.edit_delete_all_tlitts")
    ):
        raise PermissionDenied()

    if request.method == 'GET':
        serializer = TlittSerializer(tlitt)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TlittSerializer(tlitt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tlitt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#komentarze-----------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_create(request):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not (
        request.user == comment.creator
        or request.user.has_perm("tlitts.edit_delete_all_comments")
    ):
        raise PermissionDenied()

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#hashtagi------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def hashtag_list(request):
    if request.method == 'GET':
        hashtag = Hashtag.objects.all()
        serializer = HashtagSerializer(hashtag, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def hashtag_create(request):
    if request.method == 'POST':
        serializer = HashtagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def hashtag_detail(request, pk):
    try:
        hashtag = Hashtag.objects.get(pk=pk)
    except Hashtag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not (
        request.user.has_perm("tlitts.edit_delete_all_hashtag")
    ):
        raise PermissionDenied()

    if request.method == 'GET':
        serializer = HashtagSerializer(hashtag)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = HashtagSerializer(hashtag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        hashtag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#likei--------------------------------------------------------------------------------
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_list(request):
    if request.method == 'GET':
        likes = Like.objects.all()
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_create(request):
    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_detail(request, pk):
    try:
        like = Like.objects.get(pk=pk)
    except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not (request.user == like.user):
        raise PermissionDenied()

    if request.method == 'GET':
        serializer = LikeSerializer(like)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LikeSerializer(like, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#follow-----------------------------------------------------------------------------

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_list(request):
    if request.method == 'GET':
        follows = Follow.objects.all()
        serializer = FollowSerializer(follows, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_create(request):
    if request.method == 'POST':
        serializer = FollowSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_detail(request, pk):
    try:
        follow = Follow.objects.get(pk=pk)
    except Follow.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not (request.user == follow.follower):
        raise PermissionDenied()

    if request.method == 'GET':
        serializer = FollowSerializer(follow)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FollowSerializer(follow, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def feed(request):
    user = request.user
    following_ids = Follow.objects.filter(follower=user).values_list('following_id', flat=True)

    tlitts = Tlitt.objects.filter(creator__in= following_ids).order_by('-created_at')

    serializer = TlittSerializer(tlitts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def user_stats(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)

    stats = {
        "username": user.username,
        "tlitts_count": Tlitt.objects.filter(creator=user).count(),
        "followers": Follow.objects.filter(following=user).count(),
        "following": Follow.objects.filter(follower=user).count(),
        "likes_given": Like.objects.filter(user=user).count(),
    }

    return Response(stats)