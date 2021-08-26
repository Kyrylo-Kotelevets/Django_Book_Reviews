from random import randint

from authors.models import Author
from books.models import Book
from comments.models import Comment
from django.contrib.auth.models import User
from faker import Faker
from genres.models import Genre
from reviews.models import Review

fake = Faker()


def fill_genres(count: int = 20):
    """
    Creates randomly genres
    :param count: amount of genres to create
    """
    for _ in range(count):
        genre = Genre(name=fake.word().capitalize())
        genre.save()


def fill_authors(count: int = 20):
    """
    Creates randomly authors
    :param count: amount of authors to create
    """
    for _ in range(count):
        author = Author(first_name=fake.first_name(),
                        last_name=fake.last_name())
        author.save()


def fill_books(count: int = 50):
    """
    Creates randomly books
    :param count: amount of books to create
    """
    for _ in range(count):
        book = Book(title="{} {}".format(fake.word().capitalize(), " ".join(fake.words(randint(4, 12)))),
                    summary=" ".join(fake.text() for _ in range(randint(4, 10))),
                    cover_img="book_covers/random_cover_{}.jpg".format(randint(1, 6)))
        book.save()
        book.authors.add(*Author.objects.order_by('?')[:randint(1, 4)])
        book.genres.add(*Genre.objects.order_by('?')[:randint(1, 4)])
        book.save()


def fill_reviews(count: int = 100):
    """
    Creates randomly reviews
    :param count: amount of reviews to create
    """
    for _ in range(count):
        review = Review(title="{} {}".format(fake.word().capitalize(), " ".join(fake.words(randint(4, 12)))),
                        text=" ".join(fake.text() for _ in range(randint(6, 18))),
                        creator=User.objects.order_by('?')[0],
                        book=Book.objects.order_by('?')[0],
                        date_posted=fake.date_between(start_date='-10y', end_date='today'),
                        rating=randint(1, 10))
        review.save()


def fill_comments(count: int = 100):
    """
    Creates randomly comments
    :param count: amount of comments to create
    """
    for _ in range(count):
        comment = Comment(text=" ".join(fake.text() for _ in range(randint(1, 5))),
                          creator=User.objects.order_by('?')[0],
                          review=Review.objects.order_by('?')[0],
                          date_posted=fake.date_between(start_date='-10y', end_date='today'))
        comment.save()


def run():
    """
    Main function to run script
    """
    Genre.objects.all().delete()
    fill_genres(15)

    Author.objects.all().delete()
    fill_authors(15)

    Book.objects.all().delete()
    fill_books(55)

    Review.objects.all().delete()
    fill_reviews(1000)

    Comment.objects.all().delete()
    fill_comments(5000)
