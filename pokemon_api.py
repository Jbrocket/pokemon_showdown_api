from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from db_manager import db_session
from pokemon_classes import Pokemon, Move, PlayerStats, FormatStats
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
import re, requests, collections

app = Flask(__name__)
bootstrap = Bootstrap(app)
markdown = Markdown(app)
db_session.expire_on_commit = False

poke_search = ".*"
move_search = ".*"
pokemon_list = None
reverse_search = collections.defaultdict(lambda: int(1))
move_list = None
cur_format = "gen9ou"

format_list = ["randombattle", "ou", "doublesou", "ubers"]
gens = [f"gen{i}" for i in range(1, 10)]
formats = []
for format in format_list:
    for gen in gens:
        formats.append(f"{gen}{format}")
formats.append("gen9nationaldex")
formats.append("gen9nationaldexubers")
# print(formats)

def check_globals():
    global pokemon_list
    global move_list
    
    if not pokemon_list:
        pokemon_list = {}
        pokes = Pokemon.query.all()
        for num, pokemon in enumerate(pokes):
            pokemon_list[num] = pokemon
            reverse_search[pokemon.name] = num
            
    if not move_list:
        move_list = {}
        moves = Move.query.all()
        for num, move in enumerate(moves):
            move_list[num] = move
        

@app.route('/', methods=["GET"])
def home():
    return render_template('home.html')

@app.route('/pokemon/', methods=["GET", "POST"])
def pokemon():
    check_globals()
    
    if request.method == "POST":
        global poke_search
        poke_search = request.form.get("poke_search", ".*")
    
    pokemon_filtered = {}
    for key in pokemon_list:
        if re.findall(pattern=poke_search, string=pokemon_list[key].name):
            pokemon_filtered[key] = pokemon_list[key]
    return render_template('pokemon.html', poke_dict=pokemon_filtered)

@app.route('/pokemon/<int:pokemon_id>', methods=['GET'])
def pokemon_detail(pokemon_id):
    check_globals()
    return render_template('pokemon_detail.html', pokemon=pokemon_list[pokemon_id])

@app.route('/moves/', methods=["GET", "POST"])
def moves():
    check_globals()
    
    if request.method == "POST":
        global move_search
        move_search = request.form.get("move_search", ".*")
        
    moves_filtered = {}
    for key in move_list:
        if re.findall(pattern=move_search, string=move_list[key].name):
            moves_filtered[key] = move_list[key]
    return render_template('moves.html', move_dict=moves_filtered)

@app.route('/format/', methods=['GET', 'POST'])
def format():
    check_globals()
    if request.method == "POST":
        global cur_format
        cur_format = request.form.get("format", cur_format)
        
    data = requests.get(f"https://replay.pokemonshowdown.com/search.json?format={cur_format}")
    data = data.json()
    
    games = {}
    seen = collections.defaultdict(lambda: (None, int(0)))
    stats = FormatStats(cur_format)
    seen = collections.defaultdict(lambda: int(0))
    for num, game in enumerate(data):
        game_data = requests.get(f"https://replay.pokemonshowdown.com/{game['id']}.json")
        game_data = game_data.json()
        player_pokemon = set()
        
        games[f"{game_data['p1']} vs. {game_data['p2']}"] = f"https://replay.pokemonshowdown.com/{game['id']}"
        
        for line in game_data['log'].split('\n'):
            split_line = line.split('|')[1:]
            if len(split_line) < 2: continue
            if 'switch' == split_line[0]:
                player = split_line[1].split(':')[0]
                poke = split_line[2].split(',')[0]
                if (player, poke) in player_pokemon: continue
                player_pokemon.add((player, poke))
                seen[poke.lower().replace(" ","-")] += 1
            
        if num == 10:
            break
    seen = dict(sorted(seen.items(), key=lambda item: -item[1]))
    
    for num, poke in enumerate(seen):
        if num == 10: break
        stats.pokemon_list[reverse_search[poke]] = (pokemon_list[reverse_search[poke]], seen[poke])
        
    
    return render_template('format_explore.html', format=cur_format, formats=formats, games=games, format_stats=stats.pokemon_list)

@app.route('/user/', methods=['GET', 'POST'])
def user():
    check_globals()
    user_games = []
    cur_user = None
    if request.method == "POST":
        cur_user = request.form.get("username", None)
    stats = PlayerStats("")
    if cur_user:
        cur_user = "".join(cur_user.lower().split())
        data = requests.get(f"https://replay.pokemonshowdown.com/search.json?user={cur_user}")
        data = data.json()
        
        user_games = {}
        seen = collections.defaultdict(lambda: (None, int(0)))
        stats = FormatStats(cur_format)
        seen = collections.defaultdict(lambda: int(0))
        for num, game in enumerate(data):
            game_data = requests.get(f"https://replay.pokemonshowdown.com/{game['id']}.json")
            game_data = game_data.json()
            player_pokemon = set()
            users = collections.defaultdict(lambda: None)
            users["".join(game_data['p1'].lower().split())] = 'p1a'
            users["".join(game_data['p2'].lower().split())] = 'p2a'
            
            user_games[f"{game_data['p1']} vs. {game_data['p2']}"] = f"https://replay.pokemonshowdown.com/{game['id']}"
            
            for line in game_data['log'].split('\n'):
                split_line = line.split('|')[1:]
                if len(split_line) < 2: continue
                if 'switch' == split_line[0]:
                    player = split_line[1].split(':')[0]
                    if player != users[cur_user.lower()]: continue
                    poke = split_line[2].split(',')[0]
                    if (player, poke) in player_pokemon: continue
                    player_pokemon.add((player, poke))
                    seen[poke.lower().replace(" ","-")] += 1
                
            if num == 10:
                break
        seen = dict(sorted(seen.items(), key=lambda item: -item[1]))
        
        for num, poke in enumerate(seen):
            if num == 10: break
            stats.pokemon_list[reverse_search[poke]] = (pokemon_list[reverse_search[poke]], seen[poke])
        
    
    return render_template('user_explore.html', format=cur_user, games=user_games, format_stats=stats.pokemon_list)

if __name__=="__main__":
    app.run(host='0.0.0.0', port='45000')