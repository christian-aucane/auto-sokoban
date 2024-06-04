import json

class Player:
    def __init__(self, name, grids=None):
        self.name = name
        self.grids = grids if grids is not None else []

    def add_grid(self, grid, moves, time, auto_solved, cancel_count):
        self.grids.append({
            'grid': grid,
            'moves': moves,
            'time': time,
            'auto_solved': auto_solved,
            'cancel_count': cancel_count
        })

    def to_dict(self):
        return {
            'grids': self.grids,
        }

class PlayerManager:
    def __init__(self, filename):
        self.filename = filename
        self.players = self.load_players()

    def load_players(self):
        try:
            with open(self.filename, 'r') as f:
                players_data = json.load(f)
                return {name: Player(name, **data) for name, data in players_data.items()}
        except FileNotFoundError:
            return {}

    def save_players(self):
        with open(self.filename, 'w') as f:
            players_data = {name: player.to_dict() for name, player in self.players.items()}
            json.dump(players_data, f)

    def create_player(self, name):
        if name not in self.players:
            self.players[name] = Player(name)
            self.save_players()

    def delete_player(self, name):
        if name in self.players:
            del self.players[name]
            self.save_players()

    def select_player(self, name):
        return self.players.get(name)

    def get_all_players(self):
        return list(self.players.keys())
