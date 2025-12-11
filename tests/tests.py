from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from aplikacja.models import Game
from unittest.mock import patch
import projekt.game.main

class GameViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)
        self.game = Game.objects.create(current_player="o", host_player=self.user, host_player_symbol="o")
        board = projekt.game.main.nowy_board()
        self.game.set_board(board)
        self.game.save()

#       --HAPPY--

    def test_new_game_happy(self):
        url = reverse('new_game')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_board_happy(self):
        url = reverse('get_board', args=[self.game.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('board', response.text)

    def test_get_status_happy(self):
        url = reverse('get_status', args=[self.game.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('current_player', response.text)
        self.assertEqual(response.data['current_player'], "o")

    def test_join_game_happy(self):
        guest = User.objects.create_user(username="test2", password="test2" )
        self.client.force_authenticate(user=guest)
        url = reverse('join_game', args=[self.game.pk])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['game_id'], self.game.pk)
        self.game.refresh_from_db()
        self.assertEqual(self.game.guest_player, guest)

    def test_make_move_happy_move_host(self):
        self.game.host_player_symbol = "o"
        self.game.current_player = "o"
        self.game.save()
        url = reverse('make_move', args=[self.game.pk])
        coords = {"x": 0, "y": 0}
        response = self.client.post(url, coords, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "You've made your move."})
        self.game.refresh_from_db()
        self.assertEqual(self.game.get_board()[0][0], "o")
        self.assertEqual(self.game.current_player, "x")

    def test_make_move_happy_move_guest(self):
        guest = User.objects.create_user(username="guest", password="guest" )
        self.game.guest_player = guest
        self.game.host_player_symbol = "o"
        self.game.current_player = "x"
        self.game.save()
        self.client.force_authenticate(user=guest)
        url = reverse('make_move', args=[self.game.pk])
        coord = {"x": 0, "y": 0}
        response = self.client.post(url, coord, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game.refresh_from_db()
        self.assertEqual(self.game.get_board()[0][0], "x")
        self.assertEqual(self.game.current_player, "o")

    #       --SAD--

    def test_new_game_sad_bad_request_method(self):
        url = reverse('new_game')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_new_game_sad_unauthorized(self):
        self.client.logout()
        url = reverse('new_game')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_board_sad_game_not_found(self):
        id = 9999999
        url = reverse('get_board', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_board_sad_forbidden(self):
        other_id = User.objects.create_user(username="test2", password="test2" )
        self.client.force_authenticate(user=other_id)
        url = reverse('get_board', args=[self.game.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_board_sad_bad_request_method(self):
        url = reverse("get_board", args=[self.game.pk])
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_status_sad_bad_request_method(self):
        url = reverse("get_status", args=[self.game.pk])
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_status_sad_game_not_found(self):
        id = 999999
        url = reverse('get_board', args=[id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_status_sad_forbidden(self):
        other_id = User.objects.create_user(username="test2", password="test2" )
        self.client.force_authenticate(user=other_id)
        url = reverse('get_status', args=[self.game.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_join_game_sad_game_not_found(self):
        id = 9999999
        url = reverse('join_game', args=[id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_join_game_sad_bad_request_method(self):
        url = reverse("join_game", args=[self.game.pk])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_join_game_sad_host_join(self):
        url = reverse('join_game', args=[self.game.pk])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "You are the host of the game."})

    def test_join_game_sad_unauthorized(self):
        self.client.logout()
        url = reverse('join_game', args=[self.game.pk])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_join_game_sad_full_game(self):
        guest = User.objects.create_user(username="guest", password="guest" )
        self.game.guest_player = guest
        self.game.save()
        false_guest = User.objects.create_user(username="false_guest", password="false_guest")
        self.client.force_authenticate(user=false_guest)
        url = reverse('join_game', args=[self.game.pk])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "The game is already full."})

    def test_make_move_sad_game_not_found(self):
        id = 9999999
        url = reverse('make_move', args=[id])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_make_move_sad_unauthorized(self):
        self.client.logout()
        url = reverse('make_move', args=[self.game.pk])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_make_move_sad_host_move_guest(self):
        self.game.host_player_symbol = "o"
        self.game.current_player = "x"
        self.game.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('make_move', args=[self.game.pk])
        coord = {"x": 0, "y": 0}
        response = self.client.post(url, coord, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,{"message": "It's not your turn."})

    def test_make_move_sad_guest_move_host(self):
        guest = User.objects.create_user(username="guest", password="guest" )
        self.game.guest_player = guest
        self.game.host_player_symbol = "o"
        self.game.current_player = "o"
        self.game.save()
        self.client.force_authenticate(user=guest)
        url = reverse('make_move', args=[self.game.pk])
        coord = {"x": 0, "y": 0}
        response = self.client.post(url, coord, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,{"message":  "It's not your turn."})

    def test_make_move_sad_bad_request_payload(self):
        url = reverse('make_move', args=[self.game.pk])
        coord = {"x": 0}
        response = self.client.post(url, coord, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.text, '{"y":["This field is required."]}')

    def test_make_move_sad_bad_field_not_available(self):
        guest = User.objects.create_user(username="guest", password="guest" )
        self.game.guest_player = guest
        self.game.host_player_symbol = "o"
        self.game.current_player = "x"
        board = self.game.get_board()
        board[0][0] = "o"
        self.game.set_board(board)
        self.game.save()
        self.client.force_authenticate(user=guest)
        url = reverse('make_move', args=[self.game.pk])
        coord = {"x": 0, "y": 0}
        response = self.client.post(url, coord, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,{"message":  "This field is not available"})


class NewGameEndpointTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)

    @patch('aplikacja.views.rozpoczynajacy_zawodnik')
    def test_new_game_mock(self, mock_rozpoczynajacy_zawaodnik):
        mock_rozpoczynajacy_zawaodnik.return_value = "x"
        url = reverse('new_game')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_rozpoczynajacy_zawaodnik.assert_called()
        game = Game.objects.get(pk=response.data["id"])
        self.assertEqual(game.current_player, mock_rozpoczynajacy_zawaodnik.return_value)