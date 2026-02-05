from django.db import models
import json
from django.contrib.auth.models import User

class Person(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    age = models.IntegerField()
    hobby = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.name} {self.surname}'

class Address(models.Model):
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    person = models.ForeignKey(Person, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.street}, {self.city}'

class Game(models.Model):
    board = models.TextField(default = "[]")
    current_player = models.CharField(max_length = 1, choices = [("o", "player o"), ("x", "player x")])
    host_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_games")
    guest_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guest_games", null=True, blank=True)
    host_player_symbol = models.CharField(max_length=1, choices=[("o", "player o"), ("x", "player x")])
    winner = models.CharField(max_length=1, choices=[("o", "player o"), ("x", "player x")])
    is_done = models.BooleanField(default=False)

    def set_board(self, board_as_list):
        self.board = json.dumps(board_as_list)

    def get_board(self):
        return json.loads(self.board)