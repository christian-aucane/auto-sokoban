# database.py
from tinydb import TinyDB, Query

db = TinyDB('ranking_db.json')
Player = Query()

def add_player(player_id, name):
    db.insert({'id': player_id, 'name': name, 'successes': 0, 'last grid time': 0, 'last grid moves': 0})

def update_player(player_id, successes=None, time=None, moves=None):
    updates = {}
    if successes is not None:
        updates['successes'] = successes
    if time is not None:
        updates['time'] = time
    if moves is not None:
        updates['moves'] = moves
    db.update(updates, Player.id == player_id)

def get_player(player_id):
    return db.get(Player.id == player_id)

def get_all_players():
    return db.all()

def delete_player_by_name(player_name):
    db.remove(Player.name == player_name)
