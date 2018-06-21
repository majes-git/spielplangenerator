import json
import sys
from itertools import chain


class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[ERROR] %s\nAbbruch!" % str(self.message)


class schema:
    def __init__(self, schema):
        self.schema = schema
        self.count_teams()
        self.count_matches()
        self.count_rounds()

    def count_teams(self):
        '''Examine max number of teams'''
        self.teams = max(chain.from_iterable(i[:2] for i in self.schema))

    def count_matches(self):
        self.home = [0] * self.teams
        self.guest = [0] * self.teams
        self.pairs = [[0] * i for i in range(1, self.teams)]
        for match in self.schema:
            self.home[match[0] - 1] += 1
            self.guest[match[1] - 1] += 1
            if match[0] < match[1]:
                self.pairs[match[1] - 2][match[0] - 1] += 1
            elif match[0] > match[1]:
                self.pairs[match[0] - 2][match[1] - 1] += 1
            else:
                raise Error('Nicht korrekter Eintrag: %s' % match)

    def count_rounds(self):
        self.rounds = 2 * len(self.schema) / self.teams / (self.teams - 1)


def main():
    try:
        if len(sys.argv) != 2:
            print "Syntax: %s <schemaXX.json>" % sys.argv[0]
            return
        s = schema(json.load(open(sys.argv[1])))
        print '* Anzahl der Mannschaften: %d' % s.teams
        print '* Anzahl der Heim-/Gastspiele:'
        for m in range(s.teams):
            print '  - Mannschaft %2d: Heim %2d | Gast %2d | Gesamt %2d' % \
                (m + 1, s.home[m], s.guest[m], s.home[m] + s.guest[m])
        print '* Anzahl der Runden: %d' % s.rounds
        if set(chain.from_iterable(s.pairs)) != set([s.rounds]):
            raise Error('Anzahl der Paarungen (%d mal jeder gegen jeden) nicht korrekt: %s' % (s.rounds, s.pairs))
        print '* Anzahl der Paarungen (%d mal jeder gegen jeden) korrekt' % \
            s.rounds
        try:
            day = 0
            team_matches = [0] * s.teams
            for m in s.schema:
                if day != m[2]:
                    if day > m[2]:
                        raise Error('Spieltage sind nicht aufsteigend sortiert!')
                    i = 1
                    for team in team_matches:
                        if team > 2:
                            raise Error('Team %d hat mehr als 2 Spiele am %d. Spieltag!' % (i, day))
                        i += 1
                    day = m[2]
                    team_matches = [0] * s.teams
                # increase match count per team per match
                team_matches[m[0] - 1] += 1
                team_matches[m[1] - 1] += 1
        except:
            raise

    except Error, e:
        print e

if __name__ == '__main__':
    main()
