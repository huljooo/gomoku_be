from django.db import models
import json

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
    curret_player = models.CharField(max_length = 1, choices = [("o", "gracz o"), ("x", " gracz x")])

    def set_board(self, board_as_list):
        self.board = json.dumps(board_as_list)

    def get_board(self):
        return json.loads(self.board)