from datetime import date
from pymongo import MongoClient
from bson.objectid import ObjectId
from xml.dom import minidom
from models import competitionFromDict, playerFromDict, tournamentFromDict, typeOfGameFromDict
from bson.code import Code
import redis
import random
import pickle

class DB(object):
    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.r = redis.StrictRedis()
        self.db = self.connection.new_competition
        self.players = self.db.players
        self.tournaments = self.db.tournaments
        self.typesOfGame = self.db.typesOfGame
        self.competitions = self.db.competitions

    def generate(self):
        for i in range (0,50000):
            rand_player1 = random.randint(0, 5)
            rand_player2 = random.randint(0, 5)
            rand_tournament = random.randint(0, 2)
            rand_typeOfGame = random.randint(0, 2)
            player1 = self.players.find().skip(rand_player1).next()
            player2 = self.players.find().skip(rand_player2).next()
            if i % 2 == 0:
                player3 = self.players.find().skip(rand_player2).next()
            else:
                player3 = self.players.find().skip(rand_player1).next()
            tournament = self.tournaments.find().skip(rand_tournament).next()
            typeOfGame = self.typesOfGame.find().skip(rand_typeOfGame).next()
            competition = {'player1': player1, 'player2': player2, 'winner': player3,
                           'duration': random.randint(1000, 70000), 'date': date.today().strftime('%Y/%m/%d'),
                           'typeOfGame': typeOfGame['type'],
                           'tournament': tournament}
            self.competitions.insert(competition)

    def initialization(self):
        self.players.drop()
        self.tournaments.drop()
        self.typesOfGame.drop()
        self.competitions.drop()

        xmldoc = minidom.parse('tables.xml')

        player_list = xmldoc.getElementsByTagName('player')
        for player in player_list:
            playerName = str(player.getElementsByTagName('Name')[0].firstChild.data)
            playerDateOfBirth = str(player.getElementsByTagName('DateOfBirth')[0].firstChild.data)
            player = {'name': playerName, 'dateOfBirth': playerDateOfBirth}
            self.players.insert(player)

        tournament_list = xmldoc.getElementsByTagName('tournament')
        for tournament in tournament_list:
            tournamentName = str(tournament.getElementsByTagName('Name')[0].firstChild.data)
            tournamentLocation = str(tournament.getElementsByTagName('Location')[0].firstChild.data)
            tournamentDescription = str(tournament.getElementsByTagName('Description')[0].firstChild.data)
            tournamentYear = int(tournament.getElementsByTagName('Year')[0].firstChild.data)
            tournament = {'name': tournamentName, 'location': tournamentLocation,
                          'description': tournamentDescription, 'year': tournamentYear}
            self.tournaments.insert(tournament)

        typeOfGames_list = xmldoc.getElementsByTagName('typeOfGame')
        for typeOfGame in typeOfGames_list:
            typeOfGameType = str(typeOfGame.getElementsByTagName('Type')[0].firstChild.data)
            typeOfGame = {'type': typeOfGameType}
            self.typesOfGame.insert(typeOfGame)

        competition_list = xmldoc.getElementsByTagName('competition')
        for competition in competition_list:
            Player_idPlayer1 = str(competition.getElementsByTagName('Player_idPlayer1')[0].firstChild.data)
            player1 = self.players.find_one({'name': Player_idPlayer1})
            Player_idPlayer2 = str(competition.getElementsByTagName('Player_idPlayer2')[0].firstChild.data)
            player2 = self.players.find_one({'name': Player_idPlayer2})
            Player_idWinner = str(competition.getElementsByTagName('Player_idWinner')[0].firstChild.data)
            player3 = self.players.find_one({'name': Player_idWinner})
            Duration = str(competition.getElementsByTagName('Duration')[0].firstChild.data)
            Date = str(competition.getElementsByTagName('Date')[0].firstChild.data)
            TypeOfGame_idTypeOfGame = str(
                competition.getElementsByTagName('TypeOfGame_idTypeOfGame')[0].firstChild.data)
            Tournament_idTournament = str(
                competition.getElementsByTagName('Tournament_idTournament')[0].firstChild.data)
            tournament = self.tournaments.find_one({'name': Tournament_idTournament})
            competition = {'player1': player1, 'player2': player2, 'winner': player3,
                           'duration': Duration, 'date': Date, 'typeOfGame': TypeOfGame_idTypeOfGame,
                           'tournament': tournament}
            self.competitions.insert(competition)
        self.generate()

    def getCompetitionsList(self):
        competitions = []
        comp = self.competitions.find()
        for x in comp:
            competitions.append(competitionFromDict(x))
        return competitions

    def getCompetition(self, id):
        return competitionFromDict(self.competitions.find_one({'_id': id}))

    def getPlayers(self):
        players = []
        pl = self.players.find()
        for x in pl:
            players.append(playerFromDict(x))
        return players

    def getTournaments(self):
        tournaments = []
        tournam = self.tournaments.find()
        for x in tournam:
            tournaments.append(tournamentFromDict(x))
        return tournaments

    def getTypesOfGames(self):
        typesOfGame = []
        types = self.typesOfGame.find()
        for x in types:
            typesOfGame.append(typeOfGameFromDict(x))
        return typesOfGame

    def saveCompetition(self, Player_idPlayer1, Player_idPlayer2, Player_idWinner, Duration, Date,
                        TypeOfGame_idTypeOfGame, Tournament_idTournament):
        print TypeOfGame_idTypeOfGame
        player1 = self.players.find_one({'_id': Player_idPlayer1})
        player2 = self.players.find_one({"_id": Player_idPlayer2})
        player3 = self.players.find_one({"_id": Player_idWinner})
        tournament = self.tournaments.find_one({"_id": Tournament_idTournament})
        competition = self.competitions.find_one({'_id': id})
        self.r.delete(Player_idWinner)
        self.competitions.insert_one({'player1': player1, 'player2': player2, 'winner': player3,
                                      'duration': Duration, 'date': Date, 'typeOfGame': TypeOfGame_idTypeOfGame,
                                      'tournament': tournament});

    def updateCompetition(self, idCompetition, Player_idPlayer1, Player_idPlayer2, Player_idWinner, Duration, Date,
                          TypeOfGame_idTypeOfGame, Tournament_idTournament):
        player1 = self.players.find_one({"_id": Player_idPlayer1})
        player2 = self.players.find_one({"_id": Player_idPlayer2})
        player3 = self.players.find_one({"_id": Player_idWinner})
        tournament = self.tournaments.find_one({"_id": Tournament_idTournament})
        competition = self.competitions.find_one({'_id': idCompetition})
        # comp = competitionFromDict(competition)
        self.r.delete(competition["winner"]["_id"]) # .Winner.idPlayer)
        self.r.delete(Player_idWinner)
        self.competitions.replace_one({"_id": idCompetition},
                                      {'player1': player1, 'player2': player2, 'winner': player3,
                                       'duration': Duration, 'date': Date, 'typeOfGame': TypeOfGame_idTypeOfGame,
                                       'tournament': tournament});

    def removeCompetition(self, idCompetition):
        competition = self.competitions.find_one({'_id': idCompetition})
        self.r.delete(competition["winner"]["_id"])
        self.competitions.delete_one({'_id': idCompetition})

    def search(self, win_player_id):
        if self.r.exists(win_player_id) != 0:
            competitions = pickle.loads(self.r.get(win_player_id))
        else:
            query = {}
            if win_player_id != '0':
                query["winner._id"] = win_player_id # ObjectId(request.GET['client_id'])
                competitions = list(self.competitions.find(query))
            self.r.set(win_player_id,  pickle.dumps(competitions))
        new_competitions = []
        for x in competitions:
            new_competitions.append(competitionFromDict(x))
        return new_competitions
        # return list(competitions)

    def status(self, winner_id):
        if self.r.exists(winner_id) != 0:
            return 0
        else: return 1