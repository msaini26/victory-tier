"""
Contains the model used to determine who the closest basketball players are
"""
import json
import regex
from Levenshtein import ratio

class Model():
    def __init__(self, path):
        with open(path, 'r') as f:
            self.dataset = json.load(f)

    def _closest_match_levenshtein(self, query):
        """
        If the query is close to a player's full name, levenshtein distance
        will find it. It's robust to typos, but does not do well for substrings.
        """
        # Degree of similarity between query and ground-truth
        max_similarity = 0
        closest_player = None

        for player in self.dataset['Data']:
            similarity = ratio(query, player['Name'])
            if similarity > max_similarity:
                closest_player = player
                max_similarity = similarity

        return closest_player

    def _closest_match_regex(self, query):
        """
        If the query is a fuzzy substring of a player in the dataset,
        return their statistics. This is useful if the query only contains
        a single first or last name (e.g. 'lebron' => 'LeBron James').
        """
        for player in self.dataset['Data']:
            pattern = r'\b({query}){{e<=1}}\s'.format(query=query)
            pattern = regex.compile(pattern, flags=regex.IGNORECASE)
            if pattern.search(player['Name']):
                return player

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
    
    def _nearest_neighbor(self, player, k=3):
        """
        Returns the k nearest-neighbors to the given player
        """
        pass
    
    def search(self, query):
        # Match to nearest match, using minimum levenshtein distance
        player = self._closest_match(query)

        # Run a naive nearest-neighbor search
        similar_players = self._nearest_neighbor(query)

        # Return the structured players
        return {'player': player['Name']}

if __name__ == "__main__":
    """
    Some quick sanity checks
    """
    query = ''
    dummy = Model('./data/fantasy-basketball-stats.json')
    output = dummy.search(query)
    print(f"Closest player to {query} is {output['player']}")
