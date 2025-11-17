from django.test import TestCase
from catalog.models import Author, Book, BookInstance, Genre
import datetime
from django.contrib.auth.models import User


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_last_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # Исправлено: добавили слеш в конце чтобы соответствовать реальному URL
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1/')


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create an author for the book
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        # Create a book
        Book.objects.create(
            title='Test Book Title',
            author=test_author,
            summary='Test book summary',
            isbn='1234567890123'
        )

    def test_title_label(self):
        book = Book.objects.get(id=1)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        book = Book.objects.get(id=1)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=1)
        # Исправлено: добавили слеш в конце чтобы соответствовать реальному URL
        self.assertEqual(book.get_absolute_url(), '/catalog/book/1/')

    def test_display_genre(self):
        book = Book.objects.get(id=1)
        # Create some genres and add to book
        genre1 = Genre.objects.create(name='Fantasy')
        genre2 = Genre.objects.create(name='Science Fiction')
        book.genre.add(genre1, genre2)

        # Test that display_genre works (shows first 3 genres)
        self.assertEqual(book.display_genre(), 'Fantasy, Science Fiction')


class BookInstanceModelTest(TestCase):

    def setUp(self):
        # Create test data for each test method
        self.test_author = Author.objects.create(first_name='John', last_name='Smith')
        self.test_book = Book.objects.create(
            title='Test Book',
            author=self.test_author,
            summary='Test summary',
            isbn='1234567890123'
        )
        self.book_instance = BookInstance.objects.create(
            book=self.test_book,
            imprint='Test Imprint',
            due_back=datetime.date.today() + datetime.timedelta(days=7)
        )

    def test_is_overdue_property_false(self):
        """Test that is_overdue returns False for future dates"""
        # Test not overdue - future date
        self.book_instance.due_back = datetime.date.today() + datetime.timedelta(days=1)
        self.book_instance.save()
        self.assertFalse(self.book_instance.is_overdue)

    def test_is_overdue_property_true(self):
        """Test that is_overdue returns True for past dates"""
        # Test overdue - past date
        self.book_instance.due_back = datetime.date.today() - datetime.timedelta(days=1)
        self.book_instance.save()
        self.assertTrue(self.book_instance.is_overdue)

    def test_is_overdue_property_none(self):
        """Test that is_overdue returns False when due_back is None"""
        # Test when due_back is None
        self.book_instance.due_back = None
        self.book_instance.save()
        self.assertFalse(self.book_instance.is_overdue)

    def test_string_representation(self):
        expected_string = f'{self.book_instance.id} ({self.book_instance.book.title})'
        self.assertEqual(expected_string, str(self.book_instance))


class GenreModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Fantasy')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_string_representation(self):
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), 'Fantasy')