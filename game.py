from collections import defaultdict
from getpass import getpass
import random


RANDOM_PAGES = [
    "List of Sexually Active Popes",
    "List of Helicopter Escapes from Prison",
    "Wood in Popular Culture",
    "Physics Major (redirects to Engineer)",
    "US Presidents",
    "London",
    "Bank of America",
    "2007 Financial Crisis",
    "Beer"
]
random.shuffle(RANDOM_PAGES)


def random_page():
    return RANDOM_PAGES.pop()


def wiki_distance(start, target):
    return random.randint(1, 50)


def main(target, questions):
    players = []
    scores = defaultdict(int)

    for n in range(get_number(input, "How many players are present: ")):
        players.append("\033[1;{}m{}\033[0m".format(31 + n, input("\033[0mPlayer {}, what is your name: \033[1;{}m".format(n + 1, n + 31))))

    print("\033[0m")

    for n in range(questions):
        start = random_page()
        distance = wiki_distance(start, target)
        print("\033[1mQuestion {}:\033[0m How many clicks does it take to get from \033[4m{}\033[0m to \033[4m{}\033[0m?".format(str(n+1), start, target))
        question_scores = {}

        for player in players:
            guess = get_number(getpass, "{}, your guess: ".format(player))
            score = abs(guess - distance)
            question_scores[player] = score

        winner_names, winner_score = get_winners(question_scores)
        print("{} had the closest guess which was {} clicks away from the actual number of {}".format(format_list_of_names(winner_names), winner_score, distance))
        for player, score in question_scores.items():
            scores[player] += score

        if n < questions - 1:
            lead_names, lead_score = get_winners(scores)
            print("And {} {} in the lead with a score of {}".format(format_list_of_names(lead_names), "is" if len(lead_names) == 1 else "are", lead_score))

        print()  # Add a blank line to make it look nicer

    winner_names, winner_score = get_winners(scores)
    print("And {} {} the winner{} with a score of {}".format(format_list_of_names(winner_names), "is" if len(winner_names) == 1 else "are", "" if len(winner_names) == 1 else "s", winner_score))


def get_number(input_method, message):
    guess = None
    while guess is None:
        try:
            guess = int(input_method(message))
        except ValueError:
            print("You must enter a number")
    return guess


def get_winners(score_dict):
    _, lowest_score = min(score_dict.items(), key=lambda s: s[1])
    return [winner for winner, score in score_dict.items() if score == lowest_score], lowest_score


def format_list_of_names(list_of_names):
    if len(list_of_names) == 0:
        return "Nobody"
    elif len(list_of_names) == 1:
        return list_of_names[0]
    else:
        *names, last_name = list_of_names
        return "{} and {}".format(", ".join(names), last_name)


if __name__ == '__main__':
    main("Jesus", 5)
