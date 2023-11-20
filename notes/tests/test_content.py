from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestList(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Артемий Лебедев')
        cls.note_1 = Note.objects.create(title='Заголовок_1',
                                         text='Текст',
                                         slug='1',
                                         author=cls.author)
        cls.another_author = User.objects.create(
            username='Студия Артемия Лебедева'
        )
        cls.note_2 = Note.objects.create(title='Заголовок_2',
                                         text='Текст_2',
                                         slug='2',
                                         author=cls.another_author)
        cls.notes_list_url = reverse('notes:list')
        cls.author_client = Client()
        cls.another_author_client = Client()

    def test_authors_see_only_their_notes(self):
        self.another_author_client.force_login(self.another_author)
        response = self.another_author_client.get(self.notes_list_url)
        self.assertNotContains(response, self.note_1.title)
        self.assertContains(response, self.note_2.title)
        self.assertEqual(len(response.context['object_list']), 1)


"""Test of a content"""
class TestAddNotes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Артемий Лебедев')
        cls.add_note_url = reverse('notes:add')
        cls.author_client = Client()

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.add_note_url)
        self.assertIsNone(response.context)

    def test_authorized_client_has_form(self):
        self.author_client.force_login(self.author)
        response = self.author_client.get(self.add_note_url)
        self.assertIn('form', response.context)
