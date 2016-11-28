# Create your models here.

class Player:
    def __init__(self, idPlayer, name, dateOfBirth):
        self.idPlayer = idPlayer
        self.Name = name
        self.DateOfBirth = dateOfBirth


def playerFromDict(dict):
    player = Player(dict['_id'], dict['name'], dict['dateOfBirth'])
    return player


class Tournament:
    def __init__(self, idTournament, name, location, description, year):
        self.idTournament = idTournament
        self.Name = name
        self.Location = location
        self.Description = description
        self.Year = year


def tournamentFromDict(dict):
    tournament = Tournament(dict['_id'], dict['name'], dict['location'], dict['description'], dict['year'])
    return tournament


class TypeOfGame:
    def __init__(self, type):
        self.Type = type


def typeOfGameFromDict(dict):
    typeOfGame = TypeOfGame(dict['type'])
    return typeOfGame


class Competition:
    def __init__(self, idCompetition, player1, player2, winner, duration, date, typeOfGame, tournament):
        self.idCompetition = idCompetition
        self.Player1 = player1
        self.Player2 = player2
        self.Winner = winner
        self.Duration = duration
        self.Date = date
        self.Type = typeOfGame
        self.Tournament = tournament


def competitionFromDict(dict):
    competition = None
    if dict != None:
        competition = Competition(dict['_id'], playerFromDict(dict['player1']), playerFromDict(dict['player2']),
                              playerFromDict(dict['winner']), dict['duration'], dict['date'],
                              dict['typeOfGame'], tournamentFromDict(dict['tournament']))
    return competition

class AggregateEntity:
    def __init__(self, count, typeOfGame,  messages):
        self.count = count
        self.typeOfGame = typeOfGame
        self.messages = messages

def aggregateEntityFromDict(dict):
    aggregateEntity = None
    if dict != None:
        aggregateEntity = AggregateEntity(dict['count'], dict['_id'], dict['messages'])
    return aggregateEntity
