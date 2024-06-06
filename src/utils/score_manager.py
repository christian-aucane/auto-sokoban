import pandas as pd


class ScoreManager:
    COLUMNS = ["Player", "Grid", "Moves Count", "Reset Count", "Cancel Count", "Solve Used", "Execution Time"]
    def __init__(self, score_file_path=None):
        if score_file_path is not None:
            self.score_df = pd.read_csv(score_file_path)
        else:
            self.score_df = pd.DataFrame(columns=self.COLUMNS)
        self.score_file_path = score_file_path

    def add_score(self, player_name, level):
        stats = level.stats
        stats["Player Name"] = player_name
        self.score_df = self.score_df._append(stats, ignore_index=True)

    def save_scores(self):
        self.score_df.to_csv(self.score_file_path, index=False)
