from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from aplikacja.models import Game
from unittest.mock import patch

class GameViewsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)
        self.game = Game.objects.create(curret_player="o", user=self.user)

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

#       --SAD--

    def test_new_game_sad_bad_request_method(self):
        url = reverse('new_game')
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_new_game_sad_unathorized(self):
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

class NewGameEndpointTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.client.force_authenticate(user=self.user)

    @patch('aplikacja.views.rozpoczynajacy_zawodnik')
    def test_new_game_mock(self, mock_rozpoczynajcya_zawaodnik):
        mock_rozpoczynajcya_zawaodnik.return_value = "x"
        url = reverse('new_game')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_rozpoczynajcya_zawaodnik.assert_called()
        game = Game.objects.get(pk=response.data["id"])
        self.assertEqual(game.curret_player, mock_rozpoczynajcya_zawaodnik.return_value)