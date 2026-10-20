import random

class Person:
    """
    Base class to hold basic information about a person and provide comparison and string representation.
    """
    def __init__(self, name, lastname):
        self.name = name
        self.lastname = lastname

    def get_name(self):
        return f"{self.name} {self.lastname}"

    def __str__(self):
        return self.get_name()

    def __lt__(self, other):
        if self.lastname == other.lastname:
            return self.name < other.name
        return self.lastname < other.lastname

class Player(Person):
    """
    Subclass of Person, representing a basketball player with additional attributes and methods.
    """
    _id_counter = 1

    def __init__(self, name, lastname):
        super().__init__(name, lastname)
        self.shooting_power = random.randint(4, 8)
        self.points = 0
        self.points_detailed = []
        self.team = None
        self.id = Player._id_counter
        Player._id_counter += 1

    def reset(self):
        self.points = 0
        self.points_detailed = []
        self.team = None

    def get_id(self):
        return self.id

    def get_power(self):
        return self.shooting_power

    def set_team(self, team):
        self.team = team

    def get_team(self):
        return self.team

    def add_to_points(self, x):
        self.points += x
        self.points_detailed.append(x)

    def get_points_detailed(self):
        return self.points_detailed

    def get_points(self):
        return self.points

    def __lt__(self, other):
        if self.points == other.points:
            return super().__lt__(other)
        return self.points < other.points

class Manager(Person):
    """
    Subclass of Person, representing a basketball team manager with influence tracking.
    """
    _id_counter = 1

    def __init__(self, name, lastname):
        super().__init__(name, lastname)
        self.influence = 0
        self.influence_detailed = []
        self.team = None
        self.id = Manager._id_counter
        Manager._id_counter += 1

    def reset(self):
        self.influence = 0
        self.influence_detailed = []

    def get_id(self):
        return self.id

    def set_team(self, team):
        self.team = team

    def get_team(self):
        return self.team

    def add_influence(self, x):
        self.influence += x
        self.influence_detailed.append(x)

    def get_influence_detailed(self):
        return self.influence_detailed

    def get_influence(self):
        return self.influence

    def __lt__(self, other):
        if self.influence == other.influence:
            return super().__lt__(other)
        return self.influence < other.influence

class Team:
    """
    Class representing a basketball team with players, a manager, and match statistics.
    """
    _id_counter = 1

    def __init__(self, teamname, manager, players):
        self.teamname = teamname
        self.manager = manager
        self.players = players[:]
        self.fixture = []
        self.results = []
        self.wins = 0
        self.losses = 0
        self.scored = 0
        self.conceded = 0
        self.id = Team._id_counter
        Team._id_counter += 1

        # Assign this team to the manager and players
        manager.set_team(self)
        for player in players:
            player.set_team(self)

    def reset(self):
        self.fixture = []
        self.results = []
        self.wins = 0
        self.losses = 0
        self.scored = 0
        self.conceded = 0
        self.manager.reset()
        for player in self.players:
            player.reset()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.teamname

    def get_roster(self):
        return self.players

    def get_manager(self):
        return self.manager

    def add_to_fixture(self, match):
        self.fixture.append(match)

    def get_fixture(self):
        return self.fixture

    def add_result(self, result):
        self.results.append(result)
        self.scored += result[0]
        self.conceded += result[1]
        if result[0] > result[1]:
            self.wins += 1
        else:
            self.losses += 1

    def get_scored(self):
        return self.scored

    def get_conceded(self):
        return self.conceded

    def get_wins(self):
        return self.wins

    def get_losses(self):
        return self.losses

    def __str__(self):
        return self.get_name()

    def __lt__(self, other):
        if self.wins == other.wins:
            score_diff_self = self.scored - self.conceded
            score_diff_other = other.scored - other.conceded
            if score_diff_self == score_diff_other:
                return False  # Arbitrary decision
            return score_diff_self < score_diff_other
        return self.wins < other.wins

class Match:
    """
    Class representing a basketball match between two teams.
    """
    def __init__(self, home_team, away_team, week_no):
        self.home_team = home_team
        self.away_team = away_team
        self.week_no = week_no
        self.home_score = 0
        self.away_score = 0
        self.is_played_flag = False

    def is_played(self):
        return self.is_played_flag

    def play(self):
        if self.is_played_flag:
            return

        # Manager influence
        home_manager_influence = random.randint(-10, 10)
        away_manager_influence = random.randint(-10, 10)
        self.home_score += home_manager_influence
        self.away_score += away_manager_influence
        self.home_team.manager.add_influence(home_manager_influence)
        self.away_team.manager.add_influence(away_manager_influence)

        # Periods
        for _ in range(4):
            home_period_score = sum(player.get_power() + random.randint(-5, 5) for player in self.home_team.get_roster())
            away_period_score = sum(player.get_power() + random.randint(-5, 5) for player in self.away_team.get_roster())
            self.home_score += home_period_score
            self.away_score += away_period_score

        # Overtime if needed
        while self.home_score == self.away_score:
            home_overtime_score = sum(player.get_power() + random.randint(-5, 5) for player in self.home_team.get_roster())
            away_overtime_score = sum(player.get_power() + random.randint(-5, 5) for player in self.away_team.get_roster())
            self.home_score += home_overtime_score
            self.away_score += away_overtime_score

        # Update team results
        self.home_team.add_result((self.home_score, self.away_score))
        self.away_team.add_result((self.away_score, self.home_score))
        self.is_played_flag = True

    def get_match_score(self):
        return self.home_score, self.away_score

    def get_teams(self):
        return self.home_team, self.away_team
    
    def get_home_team(self):
        return self.home_team
    
    def get_away_team(self):
        return self.away_team
    
    def get_winner(self, team1, team2, is_played = False):
        self.team1 = team1
        self.team2 = team2
        self.is_played = is_played
        
        if not self.is_played:
            return None
        if self.team1.score > self.team2.score:
            return self.team1
        elif self.team2.score > self.team1.score:
            return self.team2
        return None  # Beraberlik durumu

    def __str__(self):
        if self.is_played_flag:
            return f"{self.home_team.get_name()} ({self.home_score}) vs. ({self.away_score}) {self.away_team.get_name()}"
        return f"{self.home_team.get_name()} vs. {self.away_team.get_name()}"

class Season:
    """
    Class representing a basketball season, organizing teams, matches, and fixtures.
    """
    def __init__(self, teams, managers, players):
        self.teams = []
        self.managers = []
        self.players = []
        self.fixture = []
        self.week_no = 0

        self._create_teams(teams, managers, players)
        self._build_fixture()

    def _create_teams(self, teams, managers, players):
        player_index = 0
        manager_index = 0

        for team_name in teams:
            team_players = players[player_index:player_index + 5]
            team_manager = managers[manager_index]
            self.teams.append(Team(team_name, team_manager, team_players))
            self.players.extend(team_players)
            self.managers.append(team_manager)
            player_index += 5
            manager_index += 1

    def _build_fixture(self):
        team_count = len(self.teams)
        rounds = team_count - 1
        for round_no in range(rounds * 2):
            week_matches = []
            for i in range(team_count // 2):
                home_team = self.teams[i]
                away_team = self.teams[team_count - 1 - i]
                if round_no >= rounds:
                    home_team, away_team = away_team, home_team
                match = Match(home_team, away_team, round_no + 1)
                home_team.add_to_fixture(match)
                away_team.add_to_fixture(match)
                week_matches.append(match)
            self.teams = [self.teams[0]] + [self.teams[-1]] + self.teams[1:-1]
            self.fixture.append(week_matches)

    def play_week(self):
        if self.week_no >= len(self.fixture):
            return
        for match in self.fixture[self.week_no]:
            match.play()
        self.week_no += 1

    def reset(self):
        """
        Resets all statistics about the season and returns to the original state after initialization.
        """
        self.week_no = 0
        for team in self.teams:
            team.reset_stats()
        for match_list in self.fixture:
            for match in match_list:
                match.reset()

    def get_week_no(self):
        """
        Returns the next week's number.
        """
        return self.week_no + 1

    def get_season_length(self):
        """
        Returns the number of weeks the matches will be played in the season.
        """
        return len(self.fixture)

    def get_best_player(self):
        """
        Returns the best player at the current week as a Player instance.
        """
        best_player = None
        best_performance = 0
        for player in self.players:
            if player.week_performance > best_performance:
                best_performance = player.week_performance
                best_player = player
        return best_player

    def get_best_manager(self):
        """
        Returns the best manager at the current week as a Manager instance.
        """
        best_manager = None
        best_performance = 0
        for manager in self.managers:
            if manager.week_performance > best_performance:
                best_performance = manager.week_performance
                best_manager = manager
        return best_manager

    def get_most_scoring_team(self):
        """
        Returns the most scoring team at the current week as a Team instance.
        """
        most_scoring_team = None
        highest_score = 0
        for team in self.teams:
            if team.week_score > highest_score:
                highest_score = team.week_score
                most_scoring_team = team
        return most_scoring_team

    def get_champion(self):
        """
        Returns the champion team at the end of the season as a Team instance.
        If the season is not complete, returns None.
        """
        if self.week_no < len(self.fixture):
            return None
        return max(self.teams, key=lambda team: team.season_points)

    def get_week_fixture(self, week_no):
        if 0 <= week_no < len(self.fixture):
            return self.fixture[week_no]
        return None

    def get_teams(self):
        return self.teams

    def get_players(self):
        return self.players

    def get_managers(self):
        return self.managers

    

if __name__ == "__main__":
    # Replace file reading with inline lists
    player_names = [
        "Tamir Blatt", "Malte Delow", "Marcus Eriksson", "Christ Koumadje", "Ben Lammers",
        "Erten Gazi", "Tolga Gecim", "Omer Ilyasoglu", "Shane Larkin", "Vasilje Micic",
        "Danilo Andjusic", "Dwayne Bacon", "Jerry Boutsiele", "Rudy Ballou", "Alpha Diallo",
        "Kostas Antetokounmpo", "Antoine Diot", "Youssoupha Fall", "James Gist", "Kymany Houinsou"
    ]

    team_names = [
        "ALBA Berlin", "Anadolu Efes Istanbul", "AS Monaco", "LDLC ASVEL Villeurbanne",
        "AX Armani Exchange Milan", "FC Barcelona", "Bitci Baskonia Vitoria-Gasteiz",
        "FC Bayern Munich", "CSKA Moscow", "Fenerbahce Beko Istanbul", "Crvena Zvezda mts Belgrade",
        "Maccabi Playtika Tel Aviv", "Olympiacos Piraeus", "Panathinaikos OPAP Athens", "Real Madrid",
        "UNICS Kazan", "Zalgiris Kaunas", "Zenit St Petersburg"
    ]

    manager_names = [
        "Israel Gonzalez", "Ergin Ataman", "Sasa Obradovic", "Tj Parker", "Ettore Messina",
        "Sarunas Jasikevicius", "Neven Spahija", "Andrea Trinchieri", "Dimitris Itoudis",
        "Sasa Djordjevic", "Dejan Radonjic", "Ioannis Sfairopoulos", "Georgios Bartzokas",
        "Dimitris Priftis", "Pablo Laso", "Velimir Perasovic", "Jure Zdovc", "Xavi Pascual"
    ]

    # Create managers and players
    managers = [Manager(*name.split()) for name in manager_names]
    players = [Player(*name.split()) for name in player_names]

    # Initialize the season
    season = Season(team_names, managers, players)

    # Play the season and print results
    print(season)
    for week in range(len(season.fixture)):
        print(f"\nWeek {week + 1}:")
        season.play_week()
        for match in season.get_week_fixture(week):
            print(match)

    # Display final standings
    print("\nFinal Team Standings:")
    for team in sorted(season.get_teams(), key=lambda x: (-x.get_wins(), x.get_scored() - x.get_conceded())):
        print(f"{team.get_name()} - Wins: {team.get_wins()}, Losses: {team.get_losses()}, "
              f"Scored: {team.get_scored()}, Conceded: {team.get_conceded()}")


