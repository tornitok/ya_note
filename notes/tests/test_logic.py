from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TesLogic(TestCase):
    NOTE_TEXT = 'Текст'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Author')
        cls.author_note = Note.objects.create(
            title='Заметка',
            text='Текст',
            slug=1,
            author=cls.author
        )
        cls.form_data = {
            'title': 'Заметка',
            'text': cls.NOTE_TEXT,
        }
        cls.edit_url = reverse('notes:edit', args=[cls.author_note.slug],)
        cls.delete_url = reverse('notes:delete', args=[cls.author_note.slug],)
        cls.login_url = reverse('users:login')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

    def test_anonymous_user_cant_create_note_authenticated(self):
        response = self.client.post(self.edit_url, data=self.form_data)
        url = reverse('notes:edit', args=[self.author_note.slug])
        redirect_url = f'{self.login_url}?next={url}'
        self.assertRedirects(response, redirect_url)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_user_can_create_note(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_note(self):
        response = self.author_client.post(
            self.edit_url,
            data=self.form_data
        )
        self.assertRedirects(response, reverse('notes:success'))
        self.author_note.refresh_from_db()
        self.assertEqual(self.author_note.text, self.NOTE_TEXT)

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, reverse('notes:success'))
        count = Note.objects.count()
        self.assertEqual(count, 0)

    def test_anonymous_user_cant_edit_note(self):
        response = self.client.post(
            self.edit_url,
            data=self.form_data
        )
        url = reverse('notes:edit', args=[self.author_note.slug])
        redirect_url = f'{self.login_url}?next={url}'
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.author_note.text, self.NOTE_TEXT)

    def test_anonymous_user_cant_delete_note(self):
        response = self.client.delete(self.delete_url)
        url = reverse('notes:delete', args=[self.author_note.slug])
        redirect_url = f'{self.login_url}?next={url}'
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.author_note.text, self.NOTE_TEXT)
