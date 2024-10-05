import requests
from bs4 import BeautifulSoup
import random


def print_info(right_answers, wrong_answers, total_answers):
    print('-' * 30)

    total_answers_text = f"\033[1;37;40mВсего ответов: {total_answers}\033[0m"
    print(total_answers_text.ljust(43) + "|")

    right_answers_text = f"\033[1;32;40mПравильных: {right_answers}\033[0m"
    print(right_answers_text.ljust(43) + "|")

    wrong_answers_text = f"\033[1;31;40mНе правильных: {wrong_answers}\033[0m"
    print(wrong_answers_text.ljust(43) + "|")

    percent = (right_answers / total_answers) * 100

    if percent < 40:
        color_code = "\033[1;31;40m"
    elif percent >= 40 and percent <= 60:
        color_code = "\033[1;33;40m"
    else:
        color_code = "\033[1;32;40m"

    percentage_answers_text = f"{color_code}{percent:.2f}%\033[0m"
    print(percentage_answers_text.ljust(43) + "|")

    print('-' * 30)


def learn_words():
    response = requests.get('https://online-london.com/blog/lexis/1000-slov-angliyskogo-yazyka/').text.encode('utf-8')
    soup = BeautifulSoup(response, 'lxml')
    total_answers = 0
    words = []

    for i in soup.find_all('tr'):
        if i.find_all('td'):
            en = i.find_all('td')[1].text.strip()
            ru = i.find_all('td')[2].text.strip()
            words.append((en, ru))

    right_answers = 0
    wrong_answers = 0

    while True:
        rint = random.choice((0, 1))
        r_words = random.choice(words)
        print(f"\033[1;37;40m{r_words[rint]}\033[0m")
        user_word = input()

        if user_word.lower() in r_words[1 - rint].lower() and user_word != '':
            print('\033[1;32;40mПравилно!\033[0m')
            right_answers += 1
        elif user_word == 'X':
            print_info(right_answers, wrong_answers, total_answers)
            break
        else:
            print('\033[1;31;40mОшибка\033[0m')
            print(f'\033[1;31;40mПравильный перевод: {r_words[1 - rint]}\033[0m')
            wrong_answers += 1

        total_answers = (right_answers + wrong_answers)

        if total_answers % 5 == 0:
            print_info(right_answers, wrong_answers, total_answers)


def learn_irregular_verbs():
    response = requests.get('https://ouenglish.ru/irregular-verbs').text.encode('utf-8')
    soup = BeautifulSoup(response, 'lxml')
    total_answers = 0
    words = []

    for i in soup.select('div.table-responsive tr'):
        words.append([j.text.strip() for j in i.find_all('td')[1:]])

    right_answers = 0
    wrong_answers = 0

    while True:
        r_words = random.choice(words)
        print(f"\033[1;37;40m{r_words[-1]}\033[0m")
        user_word = input().lower()

        if user_word.split() == r_words[:3]:
            print('\033[1;32;40mПравилно!\033[0m')
            right_answers += 1
        elif user_word == 'x':
            print_info(right_answers, wrong_answers, total_answers)
            break
        else:
            print('\033[1;31;40mОшибка\033[0m')
            print(f'\033[1;31;40mПравильный перевод: {" ".join(r_words[:3])}\033[0m')
            wrong_answers += 1

        total_answers = (right_answers + wrong_answers)

        if total_answers % 5 == 0:
            print_info(right_answers, wrong_answers, total_answers)


if __name__ == '__main__':
    lessons = {
        1: learn_words,
        2: learn_irregular_verbs,
    }

    print(f"1 - учить слова | 2 - учить неправильные глаголы")
    lessons[int(input())]()
