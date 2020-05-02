# Crate new 'over 65' variable for the population data
POPULATION['over_65_count']= POPULATION.iloc[:,3:].sum(axis=1)