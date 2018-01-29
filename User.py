from passlib.hash import pbkdf2_sha256
# User class containing password, preferred clubs and their user rankings,


class User:
    def __init__(self, password, id):
        # initialize list of tuples of preferred clubs and their scores
        self.ranking_list = []
        # encrypt password and store
        self.hashed_password = pbkdf2_sha256.hash(password)
        # user's year of graduation
        self.id = id

    # add new ranking into user's preferences, rankings are generated based on score from 0 to 100
    def update_club_ranking(self, club, score):
        # if club is already in list, update club ranking
        for i, ranking in enumerate(self.ranking_list):
            if ranking[0] == club:
                temp = list(self.ranking_list[i])
                temp[1] = score
                self.ranking_list[i] = tuple(temp)
                self.ranking_list = sorted(self.ranking_list, key=lambda x: x[1])
                return

        # if club is not in list, append it along with the score as a tuple and sort it
        self.ranking_list.append((club, score))
        self.ranking_list = sorted(self.ranking_list, key=lambda x: x[1], reverse=True)

    # return a list of only the names of the user ranked clubs in the order of their ranking
    def ranked_club_list(self):
        ranked_clubs = []
        for club_rank in self.ranking_list:
            ranked_clubs.append(club_rank[0])
        return ranked_clubs

    # when given a club, return the numerical ranking of that club
    def get_club_ranking(self, club):
        for i, ranking in enumerate(self.ranking_list):
            if ranking[0] == club:
                return i + 1

    # when given a club, return the numerical score of that club
    def get_club_score(self, club):
        for ranking in self.ranking_list:
            if ranking[0] == club:
                return ranking[1]

    def get_user_id(self):
        return self.id

    def print_rankings(self):
        print(self.ranking_list)

    def print_pass(self):
        print(self.hashed_password)

# For testing
#jennifer = User('ilovearun6789', 123)
# print(jennifer.get_user_id())
# jennifer.print_pass()
# jennifer.update_club_ranking('padt', 1)
# jennifer.update_club_ranking('padt', 89)
# jennifer.update_club_ranking('masti', 9)
# jennifer.update_club_ranking('masti', 90)
# jennifer.update_club_ranking('funk', 69)
# jennifer.update_club_ranking('labs', 99)
# jennifer.update_club_ranking('wppa', 29)
# jennifer.update_club_ranking('woah', 49)
# jennifer.get_club_ranking('funk')
# jennifer.get_club_score('funk')
# jennifer.ranked_club_list()
