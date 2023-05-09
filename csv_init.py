import requests
import json
import csv
import collections



if __name__ == "__main__":
    data = requests.get('https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0')
    data = data.json()
    data = data['results']
    pokemon_dict = collections.defaultdict(dict)
    
    # print(data)
    for num, pokemon in enumerate(data):
        name = pokemon['name']
        poke_data = requests.get(pokemon['url'])
        poke_data = poke_data.json()
        pokemon_dict[num] = {'name': pokemon['name'], 
                             'type1': poke_data['types'][0]['type']['name'], 
                             'type2': poke_data['types'][1]['type']['name'] if len(poke_data['types']) > 1 else "",
                             'link_normal': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{num+1}.png" if num+1 < 1011 else f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{((num+1)%1011) + 10001}.png",
                             'link_shiny': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{num+1}.png" if num+1 < 1011 else f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/{((num+1)%1011) + 10001}.png",
                             'atk': poke_data['stats'][1]['base_stat'],
                             'def': poke_data['stats'][2]['base_stat'],
                             'spdef': poke_data['stats'][3]['base_stat'],
                             'spatk': poke_data['stats'][4]['base_stat'],
                             'speed': poke_data['stats'][5]['base_stat'],
                             'hp': poke_data['stats'][0]['base_stat']
                             }
        print(pokemon_dict[num])
    # print(pokemon_dict) 
    
    
    with open('pokemon_info.csv', 'w') as csvfile:
        fieldnames = ['name', 'type1', 'type2', 'link_normal', 'link_shiny', 'atk', 'def', 'spdef', 'spatk', 'speed', 'hp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer: csv.DictWriter
        for pokemon in pokemon_dict:
            writer.writerow(pokemon_dict[pokemon])

    data =  requests.get('https://pokeapi.co/api/v2/move?limit=100000')
    data = data.json()
    data = data['results']
    moves = collections.defaultdict(dict)
    
    for num, move in enumerate(data):
        name = move['name']
        move_data = requests.get(move['url'])
        move_data = move_data.json()
        moves[num] = {
            'name': name,
            'type': move_data['type']['name'],
            'accuracy': move_data['accuracy'],
            'damage': move_data['power'],
            'pp': move_data['pp'],
            'priority': move_data['priority']
        }
        print(moves[num])
    
    
    with open('move_info.csv', 'w') as csvfile:
        fieldnames = ['name', 'type', 'accuracy', 'damage', 'pp', 'priority']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer: csv.DictWriter
        for move in moves:
            writer.writerow(moves[move])