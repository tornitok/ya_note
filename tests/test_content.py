from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from notes.models import Note
from django.contrib.auth import get_user_model

User = get_user_model()


class TestList(TestCase):
    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Артемий Лебедев')
        all_notes = [
            Note(
                title=f'Запись {index}',
                text='Просто текст.',
                slug=index,
                author=cls.author,
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
