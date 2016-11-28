from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from mongodbmanager import DB
from bson.objectid import ObjectId
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import time
from models import Player

# Create your views here.

database = DB()

def index(request):
    return render(request, 'adminpage.html',{'message':request.GET.get('message',None)})

def initializeDatabase(request):
    database.initialization()
    return redirect(reverse('index')+ '?message=Database initialized')

def listView(request):
    msgs =""
    status= ""
    if('winner_id' in request.GET and request.GET['winner_id'] != '0'):
        print request.GET['winner_id']
        if database.status(request.GET['winner_id']) == 0:
            status =  "using cash"
        else: status = "without cash"

        start_time = time.time()
        competitionsList = database.search(ObjectId(request.GET['winner_id']))
        time_res = time.time() - start_time
        msgs = str(time_res)
        print database.status(ObjectId(request.GET['winner_id']))
    else:
        competitionsList = database.getCompetitionsList()

    players = database.getPlayers()

    paginator = Paginator(competitionsList, 25)  # Show per page
    page = request.GET.get('page')
    try:
        competitions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        competitions = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        competitions = paginator.page(paginator.num_pages)

    return render(request, 'listpage.html', {'status': status, 'msgs': msgs, 'list': competitions,
                                              'players': players, 'total': str(len(competitionsList))})

    """
    list = database.getCompetitionsList()
    players = database.getPlayers()
    return render(request,'listpage.html',{'list':list, 'players':players})
    """


def removeCompetition(request, id):
    database.removeCompetition(ObjectId(id))
    return redirect(reverse('index') + '?message=Removed record')


def editCompetition(request, id):
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


