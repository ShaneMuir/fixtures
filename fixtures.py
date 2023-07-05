import itertools
import csv
from datetime import datetime, timedelta

divisions = {
    "Division 1": {
        "clubs": {
            "Club 1": {
                "teams": [
                    "team_1A",
                ],
                "tables": 1
            },
            "Club 2": {
                "teams": [
                    "team_2A"
                ],
                "tables": 1
            },
            "Club 3": {
                "teams": [
                    "team_3A"
                ],
                "tables": 1
            },
            "Club 4": {
                "teams": [
                    "team_4A",
                    "team_4B"
                ],
                "tables": 2
            },
            "Club 5": {
                "teams": [
                    "team_5A"
                ],
                "tables": 1
            },
            "Club 6": {
                "teams": [
                    "team_6A",
                    "team_6B",
                    "team_6C"
                ],
                "tables": 3
            },
            "Club 7": {
                "teams": [
                    "team_7A"
                ],
                "tables": 1
            },
            "Club 8": {
                "teams": [
                    "team_8A"
                ],
                "tables": 1
            },
            "Club 9": {
                "teams": [
                    "team_9A",
                    "team_9B"
                ],
                "tables": 2
            },
            "Club 10": {
                "teams": [
                    "DUMMY",
                ],
                "tables": 1
            }
        },
        "original_clubs": {
            "Club 1": 1,
            "Club 2": 1,
            "Club 3": 1,
            "Club 4": 2,
            "Club 5": 1,
            "Club 6": 3,
            "Club 7": 1,
            "Club 8": 1,
            "Club 9": 1,
            "Club 10": 1
        }
    },
    "Division 2": {
        "clubs": {
            "Club 10": {
                "teams": [
                    "team_10A",
                    "team_10B"
                ],
                "tables": 1
            },
            "Club 11": {
                "teams": [
                    "team_11A"
                ],
                "tables": 1
            },
            "Club 12": {
                "teams": [
                    "team_12A",
                    "team_12B"
                ],
                "tables": 2
            },
            "Club 13": {
                "teams": [
                    "team_13A"
                ],
                "tables": 1
            },
            "Club 4": {
                "teams": [
                    "team_4D",
                ],
                "tables": 2
            },
            "Club 6": {
                "teams": [
                    "team_6C",
                    "team_6D",
                    "team_6E"
                ],
                "tables": 3
            },
            "Club 14": {
                "teams": [
                    "team_14A",
                    "team_14B"
                ],
                "tables": 1
            },
            "Club 15": {
                "teams": [
                    "team_15A"
                ],
                "tables": 1
            },
            "Club 16": {
                "teams": [
                    "DUMMY"
                ],
                "tables": 1
            }
        },
        "original_clubs": {
            "Club 10": 1,
            "Club 11": 1,
            "Club 12": 2,
            "Club 13": 1,
            "Club 4": 2,
            "Club 6": 3,
            "Club 14": 1,
            "Club 15": 1,
            "Club 16": 1,
        }
    }
}

weeks_available = 34  # Weeks from September to April
match_day = "Thursday"
match_time = "8:00 PM"
start_date = datetime(2023, 9, 7)  # Start 7th of September


import random


def generate_fixture_list(weeks_available, match_day, match_time, divisions):
    fixtures = []
    for division_name, division in divisions.items():
        clubs = list(division['clubs'].keys())
        club_combinations = []
        for club_name, club in division['clubs'].items():
            for team_name in club['teams']:
                home_team = f'{club_name} {team_name}'
                for opponent_club_name, opponent_club in division['clubs'].items():
                    if club_name != opponent_club_name:
                        for opponent_team_name in opponent_club['teams']:
                            away_team = f'{opponent_club_name} {opponent_team_name}'
                            club_combinations.append((home_team, away_team))
        scheduled_games = {}
        for week in range(weeks_available):
            week_fixtures = []
            scheduled_teams = set()
            # shuffle the list of games before scheduling them
            random.shuffle(club_combinations)
            for home_team, away_team in club_combinations:
                if home_team not in scheduled_teams and away_team not in scheduled_teams:
                    # check if either team is already scheduled to play this week
                    if any(home_team in game or away_team in game for game in week_fixtures):
                        continue
                    # check if there are enough tables available at both clubs
                    home_club_name = ' '.join(home_team.split(' ')[:-1])
                    away_club_name = ' '.join(away_team.split(' ')[:-1])
                    home_tables = division['clubs'][home_club_name]['tables']
                    away_tables = division['clubs'][away_club_name]['tables']
                    if home_tables < 1 or away_tables < 1:
                        continue
                    game_key_1 = f'{home_team}-{away_team}'
                    game_key_2 = f'{away_team}-{home_team}'
                    if game_key_1 not in scheduled_games and game_key_2 not in scheduled_games:
                        week_fixtures.append((home_team, away_team))
                        scheduled_teams.add(home_team)
                        scheduled_teams.add(away_team)
                        scheduled_games[game_key_1] = True
                    elif game_key_2 not in scheduled_games:
                        week_fixtures.append((away_team, home_team))
                        scheduled_teams.add(home_team)
                        scheduled_teams.add(away_team)
                        scheduled_games[game_key_2] = True
            # check if there are fewer than 7 games this week
            if len(week_fixtures) < 7:
                print(f'Week {week + 1}: only {len(week_fixtures)} games scheduled')
                unscheduled_teams = set(clubs) - scheduled_teams
                print(f'Unscheduled teams: {unscheduled_teams}')
                unscheduled_games = [game for game in club_combinations if game[0] in unscheduled_teams or game[1] in unscheduled_teams]
                print(f'Unscheduled games: {unscheduled_games}')
            fixtures.append((division_name, week + 1, week_fixtures))
            # reset table availability for next week
            for club in clubs:
                division['clubs'][club]['tables'] = division['original_clubs'][club]
    return fixtures


def get_match_dates(start_date, weeks_available, match_day, match_time):
    match_dates = []
    current_date = start_date
    # Set the dates for the breaks
    pre_xmas_break_start = datetime(2023, 12, 8)
    pre_xmas_break_end = datetime(2023, 12, 22)
    xmas_break_start = datetime(2023, 12, 22)
    xmas_break_end = datetime(2024, 1, 5)
    post_xmas_break_start = datetime(2024, 1, 5)
    post_xmas_break_end = datetime(2024, 1, 19)

    while len(match_dates) < weeks_available:
        # Skip dates that fall within the breaks
        if pre_xmas_break_start <= current_date < pre_xmas_break_end:
            current_date += timedelta(days=1)
            continue
        if xmas_break_start <= current_date < xmas_break_end:
            current_date += timedelta(days=1)
            continue
        if post_xmas_break_start <= current_date < post_xmas_break_end:
            current_date += timedelta(days=1)
            continue

        if current_date.strftime('%A') == match_day:
            match_time_str = current_date.strftime('%Y-%m-%d') + ' ' + match_time
            match_date = datetime.strptime(match_time_str, '%Y-%m-%d %I:%M %p')
            match_dates.append(match_date)
        current_date += timedelta(days=1)
    return match_dates


def write_to_csv(fixtures, match_dates, filename):
    division_names = list(divisions.keys())
    max_week_fixtures = max([len(fixture[2]) for fixture in fixtures])
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)

        # Write header row
        header_row = ['Division', 'Week', 'Date', 'Home Team', 'Away Team'] * len(division_names)
        writer.writerow(header_row)

        # Write fixtures
        for week in range(weeks_available):
            for i in range(max_week_fixtures):
                row = []
                for division_name in division_names:
                    fixture = [f for f in fixtures if f[0] == division_name and f[1] == week + 1][0]
                    _, _, week_fixtures = fixture
                    if i < len(week_fixtures):
                        home_team, away_team = week_fixtures[i]
                        match_date = match_dates[week].strftime('%d-%m-%Y')
                        row.extend([division_name, week + 1, match_date, home_team, away_team])
                    else:
                        row.extend([''] * 5)
                writer.writerow(row)


fixtures = generate_fixture_list(weeks_available, match_day, match_time, divisions)
match_dates = get_match_dates(start_date, weeks_available, match_day, match_time)
write_to_csv(fixtures, match_dates, 'fixtures.csv')
