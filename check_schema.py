#!/usr/bin/env python

from __future__ import print_function
import json
import sys
from itertools import chain


class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "[ERROR] %s\nAbbruch!" % str(self.message)


class schema:
    def __init__(self, _schema):
        self.schema = _schema
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


def print_summary(s, all_team_days):
    print('* Anzahl der Mannschaften: %d' % s.teams)
    print('* Anzahl der Heim-/Gastspiele:')
    max_space = max([len('%s' % d) for d in all_team_days])
    for m in range(s.teams):
        team_days = all_team_days[m+1]
        max_difference = max(
            team_days[i+1]-team_days[i] for i in range(len(team_days) - 1))
        output = '  - Mannschaft {:>2}: Heim {:>2} | Gast {:>2} | Gesamt {:>2}'
        output = output.format(m + 1, s.home[m], s.guest[m],
                               s.home[m] + s.guest[m])
        output += ' => Spieltage: {:{width}} (max: {})'.format(
            team_days, max_difference, width=max_space)
        print(output)
    print('* Anzahl der Runden: %d' % s.rounds)
    if set(chain.from_iterable(s.pairs)) != set([s.rounds]):
        raise Error('Anzahl der Paarungen (%d mal jeder gegen jeden) nicht korrekt: %s' % (s.rounds, s.pairs))
    print('* Anzahl der Paarungen (%d mal jeder gegen jeden) korrekt' %
          s.rounds)


def main():
    try:
        if len(sys.argv) != 2:
            print("Syntax: %s <schemaXX.json>" % sys.argv[0])
            return
        s = schema(json.load(open(sys.argv[1])))
        try:
            day = 0
            team_matches = [0] * s.teams
            # record the match days for every team
            team_days = [[]]
            for t in range(s.teams):
                team_days.append([])
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
                if day not in team_days[m[0]]:
                    team_days[m[0]].append(day)
                if day not in team_days[m[1]]:
                    team_days[m[1]].append(day)
            print_summary(s, team_days)
        except:
            raise

    except Error, e:
        print(e)


if __name__ == '__main__':
    main()
