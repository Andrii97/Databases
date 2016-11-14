from pymongo import MongoClient
from xml.dom import minidom
from models import competitionFromDict, playerFromDict, tournamentFromDict, typeOfGameFromDict, aggregateEntityFromDict
from bson.code import Code


class DB(object):
    def __init__(self):
        self.connection = MongoClient('localhost', 27017)
        self.db = self.connection.competition
        self.players = self.db.players
        self.tournaments = self.db.tournaments
        self.typesOfGame = self.db.typesOfGame
        self.competitions = self.db.competitions

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

    def getCompetitionsList(self):
        competitions = []
        comp = self.competitions.find()
        for x in comp:
            competitions.append(competitionFromDict(x))
        return competitions

    def getCompetition(self, id):
        print self.competitions.find_one({'_id': id})
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
        self.competitions.insert_one({'player1': player1, 'player2': player2, 'winner': player3,
                                      'duration': Duration, 'date': Date, 'typeOfGame': TypeOfGame_idTypeOfGame,
                                      'tournament': tournament});

    def updateCompetition(self, idCompetition, Player_idPlayer1, Player_idPlayer2, Player_idWinner, Duration, Date,
                          TypeOfGame_idTypeOfGame, Tournament_idTournament):
        player1 = self.players.find_one({"_id": Player_idPlayer1})
        player2 = self.players.find_one({"_id": Player_idPlayer2})
        player3 = self.players.find_one({"_id": Player_idWinner})
        tournament = self.tournaments.find_one({"_id": Tournament_idTournament})
        self.competitions.replace_one({"_id": idCompetition},
                                      {'player1': player1, 'player2': player2, 'winner': player3,
                                       'duration': Duration, 'date': Date, 'typeOfGame': TypeOfGame_idTypeOfGame,
                                       'tournament': tournament});

    def removeCompetition(self, idCompetition):
        self.competitions.delete_one({'_id': idCompetition})

    def aggregationFunction(self):
        return self.competitions.aggregate([
            {"$group": {"_id": "$typeOfGame", "count":{"$sum": 1}, "messages": { "$push": {"message": "$date", "duration": "$duration"} }}},
            {"$sort": {"count": -1}}
        ])

    def count_of_winPlayer(self):
        map = Code("""
    				   function(){
    					  var winner = this.winner;
    					  emit(winner, 1);
    		           };
    		           """)

        reduce = Code("""
    					  function(key, valuesPrices){
    						var sum = 0;
    						for (var i = 0; i < valuesPrices.length; i++) {
    						  sum += valuesPrices[i];
    						}
    						return sum;
    		              };
    		              """)
        results = self.competitions.map_reduce(map, reduce, "results_")
        for doc in results.find():
            print doc
        return results

    def count_by_year(self):
        map = Code("""
    				   function(){
    					  emit(this.tournament.year, 1);
    		           };
    		           """)

        reduce = Code("""
    					  function(key, valuesPrices){
    						var sum = 0;
    						for (var i = 0; i < valuesPrices.length; i++) {
    						  sum += valuesPrices[i];
    						}
    						return sum;
    		              };
    		              """)
        results = self.competitions.map_reduce(map, reduce, "result")
        res = results.find()
        for x in res:
            print x
        return results.find()


