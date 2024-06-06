import pandas as pd


class ScoreManager:
    COLUMNS = ["Player", "Grid", "Moves", "Reset", "Cancel", "Solve", "Time"]
    def __init__(self, score_file_path=None):
        
        self.score_df = pd.DataFrame(columns=self.COLUMNS)
        if score_file_path is not None:
            if score_file_path.exists():
                self.score_df = pd.read_csv(score_file_path)
        self.score_file_path = score_file_path

    def add_score(self, player_name, level):
        stats = level.stats
        stats["Player"] = player_name
        # TODO : message d'avertissement
        self.score_df = pd.concat([self.score_df,
                                   pd.DataFrame(stats,
                                                index=[0])],
                                  ignore_index=True)

    def save_scores(self):
        self.score_df.to_csv(self.score_file_path, index=False)

    def get_scores(self, start_index=0, sort_by="Moves", ascending=False, max_scores=15):
        return self.score_df.sort_values(by=sort_by,
                                         ascending=ascending,
                                         ignore_index=True).iloc[start_index:start_index+max_scores].reset_index(drop=True)
    
    def get_columns(self):
        return self.COLUMNS
