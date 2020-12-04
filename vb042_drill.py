import datetime
import random
from termcolor import colored
import colorama
import os


class Question:
    def __init__(self, id, title, options):
        self.id = id
        self.title = title
        self.options = options

    def __str__(self):
        output_string = ''
        output_string += 'Otázka č. {0}\n'.format(self.id)
        output_string += '{0}\n'.format(self.title)

        for option in self.options:
            output_string += '{0}\n'.format(option[0])

        return output_string


def load_questions(filename):
    questions = []
    with open(filename, 'r', encoding='utf8') as f:
        content = f.read()

    question_blocks = content.split('\n\n')

    count = 0
    for question_block in question_blocks:
        if question_block.startswith('#'):
            continue
        lines = question_block.split('\n')
        options = []
        title = lines[0]

        for i in range(1, len(lines)):
            if lines[i].startswith('#') or lines[i] == '':
                continue
            tmp_option = lines[i].split('^')
            if tmp_option[1].strip() not in ['ANO', 'A', 'a', 'ano', 'NE', 'N', 'n', 'ne']:
                continue

            is_true = False
            if tmp_option[1] in ['ANO', 'A', 'a', 'ano']:
                is_true = True

            options.append((tmp_option[0].strip(), is_true))

        count += 1
        questions.append(Question(count, title, options))

    return questions


def save_score(start_time, corect_count, all_count):
    with open('statistika.txt', 'a+', encoding='utf8') as f:
        f.write('{0} {1}/{2}\n'.format(start_time.strftime('%d.%m.%Y %H:%M:%S'), corect_count, all_count))


def save_failed_answers(start_time, content):
    if not os.path.exists('reporty'):
        os.makedirs('reporty')

    with open('reporty/{0}.txt'.format(start_time.strftime('%Y-%m-%d_%H-%M-%S')), 'w', encoding='utf8') as f:
        f.write(content)


def start_test(questions):
    start_time = datetime.datetime.now()

    available_questions = []
    for i in range(0, len(questions)):
        available_questions.append(i)

    correct_count = 0
    answers_count = 0
    report_content = ''
    failed_question_ids = set()
    while len(available_questions) > 0:
        print(colored('Skóre {0}/{1} | zbývá {2} otázek'.format(correct_count, answers_count, len(available_questions)), 'green'))
        random_question = random.choice(available_questions)

        print(questions[random_question])

        print('Odpověz ano/ne nebo a/n')
        for i in questions[random_question].options:
            answers_count += 1
            print(i[0])

            answer = None
            first_answer_wrong = True
            while answer not in ['a', 'n', 'ano', 'ne']:
                answer = input().lower()

                if answer not in ['a', 'ano', 'n', 'ne']:
                    print('Odpověz ano/ne nebo a/n')
                    continue
                if (answer in ['a', 'ano']) == i[1]:
                    print(colored('Správně', 'green'))
                    correct_count += 1
                else:
                    failed_question_ids.add(questions[random_question].id-1)
                    correct = 'ANO' if i[1] else 'NE'
                    print(colored('Špatně, správně je {0}'.format(correct), 'red'))
                    if first_answer_wrong:
                        report_content += '-----------------------------------\n'
                        report_content += str(questions[random_question].title) + '\n'
                        first_answer_wrong = False
                    report_content += i[0] + '\n'
                    correct_text = 'ANO' if i[1] else 'NE'
                    report_content += 'Správná odpověď je {0}\n'.format(correct_text)

        print('Stiskni enter pro další otázku')
        input()

        available_questions.remove(random_question)
        os.system('cls' if os.name == 'nt' else 'clear')

    save_score(start_time, correct_count, answers_count)
    save_failed_answers(start_time, report_content)
    print('Skóre {0}/{1}'.format(correct_count, answers_count))
    print('Zadej a/ano pro zopakování chybných otázek, jinak něco jiného pro ukončení')
    answer = input()
    if answer.lower() in ['a', 'ano']:
        failed_questions = []
        for question_id in list(failed_question_ids):
                failed_questions.append(questions[question_id])

        start_test(failed_questions)


if __name__ == '__main__':
    colorama.init()
    questions = load_questions('vb042_dataset.txt')

    start_test(questions)
