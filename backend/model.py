"""
Contains the model used to determine who the closest basketball players are
"""
import json
import regex
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from Levenshtein import ratio

class Model():
    def __init__(self, path):
        # Load dataset
        with open(path, 'r') as f:
            self.dataset = json.load(f)
            self.dataset = pd.DataFrame(self.dataset['Data'])
            self.dataset.set_index('Name', inplace=True)

        # These features are useful for calculating distance between players
        relevant_features = [
            'Points', 'Rebounds', 'OffensiveRebounds', 'DefensiveRebounds', \
            'Assists', 'BlockedShots', 'Steals', 'Turnovers', 'FieldGoalsMade', \
            'FieldGoalsAttempted', 'FieldGoalsPercentage', 'FreeThrowsMade', \
            'FreeThrowsAttempted', 'FreeThrowsPercentage', 'TwoPointersMade', \
            'TwoPointersAttempted', 'TwoPointersPercentage', 'ThreePointersMade', \
            'ThreePointersAttempted', 'ThreePointersPercentage', 'PersonalFouls', \
            'PlusMinus', 'DoubleDoubles', 'TripleDoubles'
        ]

        # Contains normalized, preprocessed features for every player
        self.features = self._preprocess(relevant_features)

    def _preprocess(self, axes):
        """
        Create a row of features for each player. These are populated by applying
        normalization and principal component analysis to the entire dataset.

        Parameters:
            axes            Useful player statistics

        Return:
            features        A DataFrame with cleaned features for each player
        """
        # Apply normalization
        scaler = StandardScaler()
        normalized = pd.DataFrame(scaler.fit_transform(self.dataset[axes]), columns=axes, index=self.dataset.index)

        # TODO PCA
        return normalized

    def _closest_match_levenshtein(self, query):
        """
        If the query is close to a player's full name, levenshtein distance
        will find it. It's robust to typos, but does not do well for substrings.
        """
        # Degree of similarity between query and ground-truth
        max_similarity = 0
        closest_player = None

        for name, stats in self.dataset.iterrows():
            similarity = ratio(query, name)
            if similarity > max_similarity:
                closest_player = name
                max_similarity = similarity

        return closest_player

    def _closest_match_regex(self, query):
        """
        If the query is a fuzzy substring of a player in the dataset,
        return their statistics. This is useful if the query only contains
        a single first or last name (e.g. 'lebron' => 'LeBron James').
        """
        for name, stats in self.dataset.iterrows():
            pattern = r'\b({query}){{e<=1}}\s'.format(query=query)
            pattern = regex.compile(pattern, flags=regex.IGNORECASE)
            if pattern.search(name):
                return name

        return None

    def _closest_match(self, query):
        """
        Uses an ensemble of techniques to find the player object being queried
         - Ex: 'lebron' => { 'Name': 'LeBron James', 'points': '100', ... }
        """
        # First check if query is a fuzzy substring
        match = self._closest_match_regex(query)
        if match is None:
            # Get the player name with the smallest edit distance
            match = self._closest_match_levenshtein(query)
        return match

    def _norm(self, p1, p2):
        """
        Distance between two players (using l2 norm)
        """
        a = self.features.loc[[p1]]
        b = self.features.loc[[p2]]

        # Really sketchy quick l2 norm calculation
        return np.square(np.subtract(a, b)).sum(axis=1).values[0]
    
    def _nearest_neighbor(self, player, k=3):
        """
        Returns the k nearest-neighbors to the given player

        Note: Runs in O(n*log(n)) for simplicity; should be optimized
              before production usage with large datasets

        Parameters:
            player              Name of player

        Return:
            closest_players     Names of the closest k players, as a list
        """
        # Distance between current player and every other in the dataset,
        # of the form (distance, player_name)
        distances = [[self._norm(name, player), name] for name, stats in self.dataset.iterrows() if name != player]

        # Sort by distance
        distances = sorted(distances, key=lambda x: x[0], reverse=False)

        # Get the closest k players
        players = [x[1] for x in distances[:k]]

        return players


    def search(self, query):
        # Retrieve the player being queried
        queried_player = self._closest_match(query)

        # Run a naive nearest-neighbor search
        similar_players = self._nearest_neighbor(queried_player)
        similar_players = self.dataset.loc[similar_players]

        # Return the structured players
        return {'queried_player': queried_player, 'results': similar_players.to_json(orient='index')}

if __name__ == "__main__":
    """
    Some quick sanity checks
    """
    query = 'Dude'
    dummy = Model('./data/fantasy-basketball-stats.json')
    output = dummy.search(query)
    print(output)
