import itertools
from datetime import datetime, timedelta

divisions = {
    "Division 1": {
        "clubs": {
            "Club 1": 1,
            "Club 2": 1,
            "Club 3": 1,
            "Club 4": 2,
            "Club 5": 1,
            "Club 6": 3,
            "Club 7": 1,
            "Club 8": 1,
            "Club 9": 1
        },
        "original_clubs": {  # Used to reset clubs table back to original state for each week
            "Club 1": 1,
            "Club 2": 1,
            "Club 3": 1,
            "Club 4": 2,
            "Club 5": 1,
            "Club 6": 3,
            "Club 7": 1,
            "Club 8": 1,
            "Club 9": 1
        }
    },
    "Division 2": {
        "clubs": {
            "Club 10": 1,
            "Club 11": 1,
            "Club 12": 2,
            "Club 13": 1,
            "Club 4": 2,
            "Club 6": 3,
            "Club 14": 1,
            "Club 15": 1
        },
        "original_clubs": {
            "Club 10": 1,
            "Club 11": 1,
            "Club 12": 2,
            "Club 13": 1,
            "Club 4": 2,
            "Club 6": 3,
            "Club 14": 1,
            "Club 15": 1
        }
    }
}

weeks_available = 34  # Weeks from September to April
match_day = "Thursday"
match_time = "8:00 PM"
start_date = datetime(2023, 9, 7)  # Start 7th of September


def generate_fixture_list(weeks_available, match_day, match_time, divisions):
    fixtures = []
    for division_name, division in divisions.items():
        clubs = list(division['clubs'].keys())
        club_combinations = list(itertools.combinations(clubs, 2))
        scheduled_games = {}
        for week in range(weeks_available):
            week_fixtures = []
            scheduled_clubs = set()
            for home_team, away_team in club_combinations:
                if home_team not in scheduled_clubs and away_team not in scheduled_clubs:
                    home_tables = division['clubs'][home_team]
                    away_tables = division['clubs'][away_team]
                    if home_tables > 0 and away_tables > 0:
                        game_key_1 = f'{home_team}-{away_team}'
                        game_key_2 = f'{away_team}-{home_team}'
                        if game_key_1 not in scheduled_games and game_key_2 not in scheduled_games:
                            week_home_games = len([f for f in week_fixtures if f[0] == home_team])
                            if week_home_games < home_tables:
                                week_fixtures.append((home_team, away_team))
                                division['clubs'][home_team] -= 1
                                division['clubs'][away_team] -= 1
                                scheduled_clubs.add(home_team)
                                scheduled_clubs.add(away_team)
                                scheduled_games[game_key_1] = True
                        elif game_key_2 not in scheduled_games:
                            week_home_games = len([f for f in week_fixtures if f[0] == away_team])
                            if week_home_games < away_tables:
                                week_fixtures.append((away_team, home_team))
                                division['clubs'][away_team] -= 1
                                division['clubs'][home_team] -= 1
                                scheduled_clubs.add(home_team)
                                scheduled_clubs.add(away_team)
                                scheduled_games[game_key_2] = True
            fixtures.append((division_name, week + 1, week_fixtures))
            # reset table availability for next week
            for club in clubs:
                division['clubs'][club] = division['original_clubs'][club]
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
    with open(filename, 'w') as f:
        # Write header row
        for division_name in division_names:
            f.write(f'Division,Week,Date,Home Team,Away Team')
            if division_name != division_names[-1]:
                f.write(',,,,')
        f.write('\n')

        # Write fixtures
        for week in range(weeks_available):
            for i in range(max_week_fixtures):
                for division_name in division_names:
                    fixture = [f for f in fixtures if f[0] == division_name and f[1] == week + 1][0]
                    _, _, week_fixtures = fixture
                    if i < len(week_fixtures):
                        home_team, away_team = week_fixtures[i]
                        match_date = match_dates[week].strftime('%d-%m-%Y %I:%M %p')
                        f.write(f'{division_name},{week + 1},{match_date},{home_team},{away_team}')
                    else:
                        f.write(',,,,')
                    if division_name != division_names[-1]:
                        f.write(',,,,')
                f.write('\n')


fixtures = generate_fixture_list(weeks_available, match_day, match_time, divisions)
match_dates = get_match_dates(start_date, weeks_available, match_day, match_time)
write_to_csv(fixtures, match_dates, 'fixtures.csv')
