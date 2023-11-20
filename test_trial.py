# news/tests/test_trial.py
from unittest import skip

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


@skip
class Test(TestCase):

    def test_example_success(self):
        self.assertTrue(True)  # Этот тест всегда будет проходить успешно.

@skip
class YetAnotherTest(TestCase):

    def test_example_fails(self):
        self.assertTrue(False)  # Этот тест всегда будет проваливаться.

@skip
class DemonstrationExample(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()  # Вызов метода setUpClass() из родительского класса.
        # А здесь код, который подготавливает данные
        # перед выполнением тестов этого класса.

@skip
class MyTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ...

    @classmethod
    def tearDownClass(cls):
        ...  # Выполнение необходимых операций.
        super().tearDownClass()  # Вызов родительского метода.


# Импортируем функцию для определения модели пользователя

# Получаем модель пользователя.
User = get_user_model()

@skip
class TestNews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создаём пользователя.
        cls.user = User.objects.create(username='testUser')
        # Создаём объект клиента.
        cls.user_client = Client()
        # "Логинимся" в клиенте при помощи метода force_login().
        cls.user_client.force_login(cls.user)
        # Теперь через этот клиент можно отправлять запросы
        # от имени пользователя с логином "testUser".