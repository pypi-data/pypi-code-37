class Vote:
    def __init__(self, vn_id, user_id, vote, date):
        self.vn_id = vn_id
        self.user_id = user_id
        self.vote = vote
        self.date = date

    @classmethod
    def from_line(cls, line):
        parts = line.split()
        return cls(parts[0], parts[1], parts[2], parts[3])

class VoteBuilder:
    def __init__(self, vote_class=None):
        self.vote_class = vote_class or Vote
        self.votes = None

    def build_with_file_path(self, file_path):
        with open(file_path, 'r') as votes_file:
            return self.build_with_file(votes_file)

    def build_with_file(self, votes_file):
        return self.build_with_lines(votes_file.readlines())

    def build_with_lines(self, lines):
        self.votes = []
        for line in lines:
            self.votes.append(self.vote_class.from_line(line))
        return self.votes
