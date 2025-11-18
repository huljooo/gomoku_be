from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet, AddressViewSet, new_game, get_board, get_status

# @admin.register(Game)
# class GameAdmin(admin.ModelAdmin):
#     list_display = ["board", "current_player"]

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'addresses', AddressViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('game/new', new_game, name='new_game'),
    path('game/board/<int:game_id>', get_board, name='get_board'),
    path('game/status/<int:game_id>', get_status, name='get_status'),
]