import os
import json
import chess.pgn
import io

def read_from_files(dir):
    results = []
    for file in os.listdir(dir):
        file_location = dir + '/' + file
        with open(file_location) as json_file:
            read = json.load(json_file)
        results += read
    return results

def build_stats_simplified_table(members_stats):
    user_table = []
    for member in members_stats:
        if 'chess_rapid' in member['stats'].keys():
            rating_rapid = member['stats']['chess_rapid']['last']['rating']
        else:
            rating_rapid = None
        if 'chess_blitz' in member['stats'].keys():
            rating_blitz = member['stats']['chess_blitz']['last']['rating']
        else:
            rating_blitz = None
        user = {
            'username': member['username'],
            'rating_rapid': rating_rapid,
            'rating_blitz': rating_blitz
        }
        user_table.append(user)
    return user_table

def build_games_simplified_table(members_games, limit_games = 5):
    games_table = []
    n = 0
    for member in members_games:
        print('Progress: %d of %d' %(n, len(members_games)), end="\r")
        n += 1
        k = 0
        for game in member['games']:
            
            if k > limit_games:
                break

            if 'pgn' in game.keys():
                raw_pgn = game['pgn']
                eco, result, moves = process_pgn(raw_pgn)
                white_rating = game['white']['rating']
                white_user = game['white']['username']
                # white_result = game['white']['result']
                black_rating = game['black']['rating']
                black_user = game['black']['username']
                # black_result = game['black']['result']
            else:
                continue

            id = game['url'].rsplit('/', 1)[-1]
            
            if 'time_class' in game.keys():
                time_class = game['time_class']
            else:
                time_class = None

            if 'time_control' in game.keys():
                time_control = game['time_control']
            else:
                time_control = None

            if 'rules' in game.keys():
                rules = game['rules']
            else:
                rules = None

            # if 'accuracies' in game.keys():
            #     white_accuracy = game['accuracies']['white']
            #     black_accuracy = game['accuracies']['black']
            # else:
            #     white_accuracy = None
            #     black_accuracy = None

            this_game = {
                "id": id,
                "time_class" : time_class,
                "time_control" : time_control,
                "rules" : rules,
                "white_rating" : white_rating,
                "black_rating" : black_rating,
                "white_user": white_user,
                "black_user": black_user,
                # "white_result" : white_result,
                # "black_result" : black_result,
                "result": result,
                # "raw_pgn" : raw_pgn,
                "ECO": eco,
                "moves": moves
            }
            games_table.append(this_game)
            k += 1
            
    return games_table

def process_pgn(game_pgn):
    pgn = io.StringIO(game_pgn)
    game = chess.pgn.read_game(pgn)

    eco = None
    result = None
    moves = []

    if 'ECO' in game.headers.keys():
        eco = game.headers['ECO']

    if 'Result' in game.headers.keys():
        result = game.headers['Result']

    for move in game.mainline_moves():
        moves.append(move.uci())
    
    return eco, result, moves
                



