from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Person, Address, Game
from .serializers import PersonSerializer, AddressSerializer, CoordinateSerializer
from gomoku_be.game.main import rozpoczynajacy_zawodnik, nowy_board, czy_wygral
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def logout_user(request):
    logout(request)
    return redirect("login_user")


def login_user(request):
    if request.user.is_authenticated:
        return redirect("lobby")
    else:
        return render(request, "aplikacja/login_user.html", {'bad_creds': "bad_creds" in request.GET})


def check_creds(request):
    user = authenticate(username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect("lobby")
    else:
        url = reverse('login_user') + "?bad_creds=1"
        return redirect(url)


@login_required(login_url='login_user')
def lobby(request):
    games = Game.objects.filter(is_done=False, guest_player__isnull=True)
    return render(request, "aplikacja/lobby.html", {'games':games})


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [IsAuthenticated]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_game(request):
    game = Game(current_player=rozpoczynajacy_zawodnik(), host_player=request.user,
                host_player_symbol=rozpoczynajacy_zawodnik())
    game.set_board(nowy_board())
    game.save()
    return Response({"id": game.pk})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_board(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist.")
    if game.host_player != request.user and request.user != game.guest_player:
        raise PermissionDenied("It's not your game.")

    return Response({"board": game.get_board()})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_status(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist.")
    if game.host_player != request.user and request.user != game.guest_player:
        raise PermissionDenied("It's not your game.")

    winner_user = None
    winner_symbol = None

    if game.is_done and game.winner:
        winner_symbol = game.winner
        if winner_symbol == game.host_player_symbol:
            winner_user = game.host_player.username
        else:
            winner_user = game.guest_player.username

    return Response({"current_player": game.current_player,
                     "is_done": game.is_done,
                     "winner_symbol": winner_symbol,
                     "winner_user": winner_user})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist.")

    if game.is_done:
        return Response({"message": "This game is already finished"}, status=status.HTTP_400_BAD_REQUEST)

    if game.host_player == request.user:
        return Response({"message": "You are the host of the game."})

    if game.guest_player:
        return Response({"message": "The game is already full."})

    game.guest_player = request.user
    game.save()

    return Response({"game_id": game.pk})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_move(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist.")

    if game.is_done:
        return Response({"message": "This game is already finished"}, status=status.HTTP_400_BAD_REQUEST)

    if request.user != game.host_player and request.user != game.guest_player:
        return Response({"message": "You don't have permission to play this game."})

    if request.user == game.host_player:
        symbol = game.host_player_symbol
    else:
        if game.host_player_symbol == "x":
            symbol = "o"
        else:
            symbol = "x"

    if symbol != game.current_player:
        return Response({"message": "It's not your turn."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CoordinateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    x = request.data["x"]
    y = request.data["y"]
    board = game.get_board()
    if board[x][y] != ".":
        return Response({"message": "This field is not available"}, status=status.HTTP_400_BAD_REQUEST)
    board[x][y] = symbol
    game.set_board(board)
    game.current_player = "x" if symbol == "o" else "o"
    if czy_wygral(symbol, board):
        game.is_done = True
        game.winner = symbol
    game.save()

    return Response({"message": "You've made your move.",
                     "is_done": game.is_done,
                     "winner_symbol": game.winner,
                     "winner_user": request.user.username if game.is_done else None})
