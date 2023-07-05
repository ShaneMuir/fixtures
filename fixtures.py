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
        for week in range(weeks_available):
            week_fixtures = []
            for home_team, away_team in club_combinations:
                home_tables = division['clubs'][home_team]
                away_tables = division['clubs'][away_team]
                if home_tables > 0 and away_tables > 0:
                    week_fixtures.append((home_team, away_team))
                    division['clubs'][home_team] -= 1
                    division['clubs'][away_team] -= 1
            fixtures.append((division_name, week + 1, week_fixtures))
    return fixtures


def get_match_dates(start_date, weeks_available, match_day, match_time):
    match_dates = []
    current_date = start_date
    while len(match_dates) < weeks_available:
        if current_date.strftime('%A') == match_day:
            match_time_str = current_date.strftime('%Y-%m-%d') + ' ' + match_time
            match_date = datetime.strptime(match_time_str, '%Y-%m-%d %I:%M %p')
            match_dates.append(match_date)
        current_date += timedelta(days=1)
    return match_dates


def write_to_csv(fixtures, match_dates, filename):
    with open(filename, 'w') as f:
        f.write('Division,Week,Date,Home Team,Away Team\n')
        for fixture in fixtures:
            division_name, week, week_fixtures = fixture
            match_date = match_dates[week - 1].strftime('%Y-%m-%d %I:%M %p')
            for home_team, away_team in week_fixtures:
                f.write(f'{division_name},{week},{match_date},{home_team},{away_team}\n')


fixtures = generate_fixture_list(weeks_available, match_day, match_time, divisions)
match_dates = get_match_dates(start_date, weeks_available, match_day, match_time)
write_to_csv(fixtures, match_dates, 'fixtures.csv')
