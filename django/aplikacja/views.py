from rest_framework.decorators import api_view, permission_classes
from django.http import Http404
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
    game = Game(curret_player=rozpoczynajacy_zawodnik())
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

    return Response({"board": game.get_board()})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_status(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404("Game does not exist")

    return Response({"current_player": game.curret_player})
