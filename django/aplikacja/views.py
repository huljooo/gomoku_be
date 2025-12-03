from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Person, Address, Game
from .serializers import PersonSerializer, AddressSerializer
from projekt.game.main import rozpoczynajacy_zawodnik, nowy_board

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
    game = Game(curret_player=rozpoczynajacy_zawodnik(), host_player=request.user, host_player_symbol=rozpoczynajacy_zawodnik())
    game.set_board(nowy_board())
    game.save()
    return Response({"id": game.pk})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_board(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    if game.host_player != request.user and request.user != game.guest_player:
        raise PermissionDenied("To nie twoja gra")

    return Response({"board": game.get_board()})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_status(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")
    if game.host_player != request.user and request.user != game.guest_player:
        raise PermissionDenied("To nie twoja gra")

    return Response({"current_player": game.curret_player})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_game(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    if game.host_player == request.user:
        return Response("Jesteś hostem gry")

    if game.guest_player:
        return Response("Gra juz jest pełna")

    game.guest_player = request.user
    game.save()

    return Response({"game_id": game.pk})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_move(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    if request.user != game.host_player and request.user != game.guest_player:
        return Response("Nie masz uprawnien do tej gry")

    if request.user == game.host_player:
        symbol = game.host_player_symbol
    else:
        if game.host_player_symbol == "x":
            symbol = "o"
        else:
            symbol = "x"

    if symbol != game.curret_player:
        return Response("To nie twoja kolej")

    x = request.data["x"]
    y = request.data["y"]
    board = game.get_board()
    board[x][y] = symbol
    game.set_board(board)
    game.curret_player = "x" if symbol == "o" else "o"
    game.save()

    return Response("jest w pyte")