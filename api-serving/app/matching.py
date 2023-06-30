import pandas as pd
from fuzzywuzzy import fuzz, process


class FuzzyMatch:
    def __init__(self, csvfile, input, output):
        self.df = pd.read_csv(csvfile)
        self.input = input
        self.output = output
    
    def match(self, query, num_matches=1):
        match_results = process.extract(query, self.df[self.input], scorer=fuzz.partial_ratio)
        sorted_results = sorted(match_results, key=lambda x: x[1], reverse=True)
        closest_matches = sorted_results[:num_matches]
        return [self.df.loc[match[2], self.output] for match in closest_matches]
        
        