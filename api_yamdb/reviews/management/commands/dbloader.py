from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Title, Category, Genre, Comment, Review
from users.models import User

'''Скрипт для импорта csv-файлов в базу данных sqlite3'''
'''Запуск скрипта через команду "python manage.py dbloader" в консоле'''


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        with open('static/data/category.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                category = Category(id=id, name=name, slug=slug)
                category.save()
                self.stdout.write(
                    "!!!The category database has been loaded successfully!!!")

        with open('static/data/genre.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                genre = Genre(id=id, name=name, slug=slug)
                genre.save()
                self.stdout.write(
                    "!!!The genre database has been loaded successfully!!!")

        with open('static/data/titles.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category_id = row['category']
                title = Title(id=id, name=name, year=year,
                              category_id=category_id)
                title.save()
                self.stdout.write(
                    "!!!The title database has been loaded successfully!!!")

        with open('static/data/genre_title.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                Title.objects.get(
                    id=row['title_id']).genre.add(row['genre_id'])
                self.stdout.write(
                    "!!!The genretitle database has been"
                    "loaded successfully!!!")

        with open('static/data/users.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                user = User(id=id, username=username, email=email, role=role,
                            bio=bio, first_name=first_name,
                            last_name=last_name)
                user.save()
                self.stdout.write(
                    "!!!The user database has been loaded successfully!!!")

        with open('static/data/review.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                review = Review()
                review.title = Title.objects.get(id=row['title_id'])
                review.id = row['id']
                review.text = row['text']
                review.score = row['score']
                review.pub_date = row['pub_date']
                review.author = User.objects.get(id=row['author'])
                review.save()
                self.stdout.write(
                    "!!!The review database has been loaded successfully!!!")

        with open('static/data/comments.csv', encoding='utf8') as csv_file:
            csv_reader = DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                comment = Comment()
                comment.id = row['id']
                comment.text = row['text']
                comment.pub_date = row['pub_date']
                comment.author = User.objects.get(id=row['author'])
                comment.review = Review.objects.get(id=row['review_id'])
                comment.save()
                self.stdout.write(
                    "!!!The comment database has been loaded successfully!!!")
