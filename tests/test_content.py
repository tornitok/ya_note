from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class TestList(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        today = datetime.today()
        cls.author = User.objects.create(username='Артемий Лебедев')
        all_notes = [
            Note(
                title=f'Запись {index}',
                text='Просто текст.',
                slug=index,
                author=cls.author,
                date=today - timedelta(days=index)
            )
            for index in range(settings.NOTES_COUNT_ON_LIST_PAGE)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['notes_list']
        notes_count = len(object_list)
        self.assertEqual(notes_count, settings.NOTES_COUNT_ON_LIST_PAGE)

    def test_order_notes(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)



class TestDetailPage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Артемий Лебедев')
        cls.detail_url = reverse('notes:form')

    def test_anonymous_client_has_no_form(self):
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)
