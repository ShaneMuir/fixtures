import csv
from itertools import combinations

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

weeks_available = 100  # Total number of weeks available for matches

# Step 2: Create a list of teams for each division
team_list = {}
for division, data in divisions.items():
    team_list[division] = list(data["clubs"].keys())

# Step 3: Generate round-robin schedule for each division
fixtures = {}
for division, teams in team_list.items():
    fixtures[division] = list(combinations(teams, 2))


# Step 4: Adjust the schedule for clubs with limited tables
def distribute_matches(division, club, matches):
    club_tables = divisions[division]["clubs"][club]
    home_matches = matches[:club_tables]
    away_matches = matches[club_tables:]
    return list(zip(home_matches, away_matches)) + list(zip(away_matches, home_matches))


# Step 5: Adjust the schedule for clubs with limited tables
for division, data in divisions.items():
    division_matches = fixtures[division]  # Store the matches for the division separately
    updated_matches = division_matches  # Create a separate list for updating the matches
    distributed_matches = []  # List to track the distributed matches
    for club, tables in data["clubs"].items():
        if tables < len(team_list[division]):
            matches = [match for match in division_matches if club in match]
            distributed = distribute_matches(division, club, matches)
            distributed_matches.extend(distributed)
    updated_matches = [match for match in updated_matches if match not in distributed_matches]
    updated_matches.extend(distributed_matches)
    fixtures[division] = updated_matches  # Update the fixtures dictionary

# Step 6: Assign dates to the fixture list
match_dates = {}
match_day = "Thursday"
match_time = "8:00 PM"

for division, matches in fixtures.items():
    num_matches = len(matches)

    if num_matches > 0:  # Add check for zero matches
        weeks_per_match = weeks_available // num_matches

        if weeks_per_match == 0:  # Handle zero division error
            print(f"Not enough weeks available for matches in {division}")
            continue

        match_dates[division] = []

        for i, match in enumerate(matches, start=1):
            week = (i - 1) % weeks_per_match + 1
            date = f"Week {week}"
            match_dates[division].append((date, match))

# Step 7: Store the fixture list in a CSV file
filename = "fixtures.csv"

with open(filename, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Division", "Date", "Home Club", "Away Club"])

    for division, dates in match_dates.items():
        for date, match in dates:
            for teams in match:
                writer.writerow([division, date, teams[0], teams[1]])
