from chessdotcom import get_player_profile, get_club_members, get_player_stats, get_player_game_archives, get_player_games_by_month, get_player_games_by_month_pgn

def get_list_of_club_members(clubID):
    response = get_club_members(clubID).json
    members = response['members']['all_time']
    return members

def get_club_members_stats(users):
    k = 1
    members_stats = []
    for user in users:
        username = user['username']
        response = get_player_stats(username).json
        member_stats = {
            'username': username,
            'stats': response['stats']
        }
        members_stats.append(member_stats)
        print("Progress: %d of %d users fetched" %(k, len(users)), end = "\r")
        k += 1
    print("\n---")
    return members_stats

def get_club_members_monthly_games(users, year, month):
    k = 0
    members_games = []
    for user in users:
        username = user['username']
        try:
            response = get_player_games_by_month(username, year=year, month=month).json
            member_games = {
                'username': username,
                'games': response['games']
            }
        except:
            member_games = {
                'username': username,
                'games': []
            }
            print('Error retrieving user')
        members_games.append(member_games)
        print("Progress: %d of %d users fetched" %(k + 1, len(users) + 1), end = "\r")
        k += 1
    print("\n---")
    return members_games

def player_stats(username):
    response = get_player_stats(username).json
    return response

def player_profile(username):
    response = get_player_profile(username).json
    return response