import datetime

from django.test import TestCase

# Create your tests here.

from django.utils import timezone

from .models import Question

'''
https://docs.djangoproject.com/en/2.2/intro/tutorial05/#create-a-test-to-expose-the-bug

    A conventional place for an application’s tests is in the application’s
    tests.py file; the testing system will automatically find tests
    in any file whose name begins with test.

    注: the testing system 将 自动的 查找 任何 文件名 以 test 开始的 文件中的 tests

https://docs.djangoproject.com/en/2.2/intro/tutorial05/#running-tests

跑测试(run tests) 的命令:
(tutorial-venv) [root@python3lang mysite]# python manage.py test polls


执行该 测试命令后 所发生的事情:
    - manage.py test polls looked for tests in the polls application
    - it found a subclass of the django.test.TestCase class
    - it created a special database for the purpose of testing
    - it looked for test methods - ones whose names begin with test
    - in test_was_published_recently_with_future_question it created
      a Question instance whose pub_date field is 30 days in the future
    - … and using the assertIs() method, it discovered that its was_published_recently()
      returns True, though we wanted it to return False

'''


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
