# Crate new 'over 65' variable for the population data
POPULATION['over_65_count'] = POPULATION.iloc[:, 3:].sum(axis=1)


# As some values have been withheld (but should add to 100), infer them from the other two 
INTERNET_USE_LA['WEEKLY_OR_LESS_PCT'] = 100 - INTERNET_USE_LA.iloc[:,2] - INTERNET_USE_LA.iloc[:,1]
