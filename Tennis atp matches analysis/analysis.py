import csv
import io
from urllib.request import urlopen

matches = []
for x in range(2012, 2018):
    #Get csv from git using urllib.request
    response = urlopen(f'https://raw.githubusercontent.com/DexterHyde/Python-Data-Engineering-Projects/master/Tennis%20atp%20matches%20analysis/atp_matches_{x}.csv')
    #Need io because some csv files are weird
    f = csv.reader(io.TextIOWrapper(response, encoding='utf-8'))
    #Save and print the categories
    categories = next(f)
    print(f'Categories {x}: {categories}')
    #Save match data in dictionaries
    for line in f:
        matches.append({c: li for c, li in zip(categories, line)})


#Get all winners and losers
winners = [match['winner_name'] for match in matches]
print(f'\nWinners: {winners}\n')
losers = [match['loser_name'] for match in matches]
print(f'Losers: {losers}\n')

#Get winners who didn't lose a single match
#This could also be done with a hashmap (dictionary)
bestPlayers = [best for best in set(winners) if best not in losers]
print(f'Best Players: {bestPlayers}\nTotal # of best players: {len(bestPlayers)}')

#Get players who didn't win a single match
#This could also be done with a hashmap (dictionary)
badPlayers = [player for player in set(losers) if player not in winners]
print(f'Worst Players: {badPlayers}\nTotal # of worst players: {len(badPlayers)}')

#json in which each key is the name of the player and the item is the total of won matches
howManyMatchesWon = {c: winners.count(c) for c in set(winners)}
print(f'\nMatches won by player:{howManyMatchesWon}')

#json in which each key is the name of the player and the item is the total of lost matches
howManyMatchesLost = {c: losers.count(c) for c in set(losers)}
print(f'\nMatches lost by player:{howManyMatchesLost}')

#Get the player that won the most matches from 2012 to 2017:
bestPlayer = max(howManyMatchesWon, key = howManyMatchesWon.get)
print(f'\nThe best player is: {bestPlayer} with a total of {howManyMatchesWon[bestPlayer]} matches won')

#Get the player that lost the most matches from 2012 to 2017:
worstPlayer = max(howManyMatchesLost, key = howManyMatchesLost.get)
print(f'\nThe worst player is: {worstPlayer} with a total of {howManyMatchesLost[worstPlayer]} matches lost')

#Obtain all players that have played a semifinal:
semiWinners = {match['winner_name'] for match in matches if match.get('round') == 'SF'}
semiLosers = {match['loser_name'] for match in matches if match.get('round') == 'SF'}
semi = semiWinners | semiLosers
print(f'\nAll players that have played in a semifinal: {semi}')

#Obtain all players that've won at least one final
champions = {match['winner_name'] for match in matches if match.get('round') == 'F'}
print(f'\nAll players that have won a final: {champions}\n')

#Get the 10 best players that have won the most matches:
sortedPlayers = sorted(howManyMatchesWon, key = howManyMatchesWon.get, reverse = True)
print('\nTop 10 Best Players:\n')
[print(f'{player} with {howManyMatchesWon[player]} matches won') for player in sortedPlayers[:10]]

#Get the 10 worst players that have won the most matches:
sortedPlayers = sorted(howManyMatchesLost, key = howManyMatchesLost.get, reverse = True)
print('\nTop 10 worst Players:\n')
[print(f'{player} with {howManyMatchesWon[player]} matches lost') for player in sortedPlayers[:10]]

#Get unique surface types
surfaces = {match['surface'] for match in matches}
print(f'\nSurface types:\n{surfaces}')

#For each surface type obtain the 3 best players with most won finals and the number of said won finals
#It's kind of random but it shall be interesting to get
verySpecific = []
for surface in list(surfaces)[1:]:
    winnersPerSurface = [match['winner_name'] for match in matches if match['surface'] == surface and match.get('round') == 'F']
    countedWinners = [{'Player': player, 'Won Matches': winnersPerSurface.count(player)} for player in set(winnersPerSurface)]
    verySpecific.append({'Surface Type': surface, 'Best Players': sorted(countedWinners, key = lambda x: x['Won Matches'], reverse = True)[:3]})

print('\nBest 3 top players for each surface type')

print('\n'.join([str(x) for x in verySpecific]))