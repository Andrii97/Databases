from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mongodbmanager import DB
from bson.objectid import ObjectId
import time
# Create your views here.

def index(request):
    return render(request, 'adminpage.html',{'message':request.GET.get('message',None)})

def initializeDatabase(request):
    database = DB()
    database.initialization()
    return redirect(reverse('index')+ '?message=Database initialized')

def listView(request):
    database = DB()
    list = database.getCompetitionsList()
    return render(request,'listpage.html',{'list':list})

def aggregateAndMapReduce(request):
    database = DB()
    aggregationList = database.aggregationFunction()
    print "aggregate"
    for a in aggregationList:
        print a
    print "map reduce 1"
    database.count_by_year()
    print "map reduce 2"
    database.count_of_winPlayer()
    return redirect(reverse('index') + '?message=aggregation and map reduce functions was calculated and show',
    {"list": aggregationList})



def removeCompetition(request, id):
    database = DB()
    database.removeCompetition(ObjectId(id))
    return redirect(reverse('index') + '?message=Removed record')


def editCompetition(request, id):
    database = DB()
    if request.method == 'GET':
        players = database.getPlayers()
        typesOfGames = database.getTypesOfGames()
        tournaments = database.getTournaments()
        print id
        competition = database.getCompetition(ObjectId(id))
        return render(request,'editCompetition.html', {'player1':players, 'player2':players, 'playerWin':players,
                                                       'typesOfGame':typesOfGames, 'tournaments':tournaments,
                                                       'competition':competition})
    else:
        database.updateCompetition(ObjectId(id), ObjectId(request.POST['idPlayer1']), ObjectId(request.POST['idPlayer2']),
                                   ObjectId(request.POST['idPlayerWin']), request.POST['duration'],
                                   str(time.strftime("%Y-%m-%d")), request.POST['idTypeOfGame'],
                                   ObjectId(request.POST['idTournament']))
        return redirect(reverse('index') + '?message=Changed Competition')


def addCompetition(request):
    database = DB()
    if request.method == 'GET':
        players = database.getPlayers()
        typesOfGames = database.getTypesOfGames()
        tournaments = database.getTournaments()
        return render(request,'addCompetition.html', {'player1':players, 'player2':players, 'playerWin':players,
                                                      'typesOfGame':typesOfGames, 'tournaments':tournaments})
    elif request.method == 'POST':
        database.saveCompetition(ObjectId(request.POST['idPlayer1']), ObjectId(request.POST['idPlayer2']),
                                 ObjectId(request.POST['idPlayerWin']), request.POST['duration'],
                                 str(time.strftime("%Y-%m-%d")), request.POST['idTypeOfGame'],
                                 ObjectId(request.POST['idTournament']))
        return redirect(reverse('index') + '?message=Added Competition')


