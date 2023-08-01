import csv

from django.core.management.base import BaseCommand, CommandError
from polls.models import Question, Choice


class Command(BaseCommand):
    help = "Takes an input file and loads all the questions and choices from it"

    def add_arguments(self, parser):
        parser.add_argument("--filename", "-f", nargs="?", type=str)

    def handle(self, *args, **options):
        filename = options["filename"]
        if not filename:
            raise CommandError('Command must be provided with a filename!')

        with open(f"./{filename}", mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # question_column, c_columns = row.split(',', 1)
                    # choice_columns = [c.strip() for c in c_columns.split(',')]
                    line_count += 1
                question, choices = row[0], row[1:]
                q = Question.objects.create(question_text=question.strip())
                for choice in [c.strip() for c in choices]:
                    Choice.objects.create(question=q, choice_text=choice)
                line_count += 1
            print(f'Processed {line_count} lines.')
        print('Successfully added all questions and choices!')
