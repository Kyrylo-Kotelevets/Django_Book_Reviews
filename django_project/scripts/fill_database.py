from reviews.models import Genre, Author, Book, Review, Comment
from django.contrib.auth.models import User
from random import randint
from faker import Faker

fake = Faker()


def fill_genres(count: int = 20):
    for _ in range(count):
        genre = Genre(name=fake.word().capitalize())
        genre.save()


def fill_authors(count: int = 20):
    for _ in range(count):
        author = Author(first_name=fake.first_name(),
                        last_name=fake.last_name())
        author.save()


def fill_books(count: int = 50):
    for _ in range(count):
        book = Book(title="{} {}".format(fake.word().capitalize(), " ".join(fake.words(randint(4, 12)))),
                    rating=randint(1000, 2000),
                    summary=" ".join(fake.text() for _ in range(randint(4, 10))))
        book.save()


def fill_reviews(count: int = 100):
    for _ in range(count):
        review = Review(title="{} {}".format(fake.word().capitalize(), " ".join(fake.words(randint(4, 12)))),
                        text=" ".join(fake.text() for _ in range(randint(6, 18))),
                        creator=User.objects.order_by('?')[0],
                        book=Book.objects.order_by('?')[0],
                        date_posted=fake.date_between(start_date='-10y', end_date='today'),
                        rating=randint(1, 10))
        review.save()


def fill_comments(count: int = 100):
    for _ in range(count):
        comment = Comment(text=" ".join(fake.text() for _ in range(randint(1, 5))),
                          creator=User.objects.order_by('?')[0],
                          review=Review.objects.order_by('?')[0],
                          date_posted=fake.date_between(start_date='-10y', end_date='today'))
        comment.save()


Genre.objects.all().delete()
fill_genres(15)

Author.objects.all().delete()
fill_authors(15)

Book.objects.all().delete()
fill_books(35)

Review.objects.all().delete()
fill_reviews(200)

Comment.objects.all().delete()
fill_comments(2000)
