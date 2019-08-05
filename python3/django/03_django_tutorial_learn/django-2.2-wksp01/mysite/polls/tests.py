import datetime

from django.test import TestCase

# Create your tests here.
from django.urls import reverse

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

    '''
    The Django test client

    https://docs.djangoproject.com/en/2.2/intro/tutorial05/#the-django-test-client

      Django provides a test Client to simulate a user interacting with the code
      at the view level. We can use it in tests.py or even in the shell.

      在 Django shell 中使用 client 的方式:

(tutorial-venv) [root@python3lang mysite]# python manage.py shell
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()

函数 setup_test_environment 的 作用:
    https://docs.djangoproject.com/en/2.2/topics/testing/advanced/#django.test.utils.setup_test_environment

    setup_test_environment() installs a template renderer which will
    allow us to examine some additional attributes on responses such as
    response.context that otherwise wouldn’t be available. Note that this
    method does not setup a test database, so the following will be
    run against the existing database and the output may differ slightly
    depending on what questions you already created. You might get unexpected
    results if your TIME_ZONE in settings.py isn’t correct. If you don’t
    remember setting it earlier, check it before continuing.

    注: 这种方式不会 setup a test database, 所以如下这种方式 是在 现有的 database 上跑命令的.

Next we need to import the test client class (later in tests.py we will use
the django.test.TestCase class, which comes with its own client, so this won’t be required):

>>> from django.test import Client
>>> # create an instance of the client for our use
>>> client = Client()

With that ready, we can ask the client to do some work for us:

>>> # get a response from '/'
>>> response = client.get('/')
Not Found: /
>>> # we should expect a 404 from that address; if you instead see an
>>> # "Invalid HTTP_HOST header" error and a 400 response, you probably
>>> # omitted the setup_test_environment() call described earlier.
>>> response.status_code
404
>>> # on the other hand we should expect to find something at '/polls/'
>>> # we'll use 'reverse()' rather than a hardcoded URL
>>> from django.urls import reverse
>>> response = client.get(reverse('polls:index'))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/1/">What&#39;s up?</a></li>\n    \n    </ul>\n\n'
>>> response.context['latest_question_list']
<QuerySet [<Question: What's up?>]>


    '''


# https://docs.djangoproject.com/en/2.2/intro/tutorial05/#testing-our-new-view
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


# Testing our new view
# https://docs.djangoproject.com/en/2.2/intro/tutorial05/#testing-our-new-view
# 一个很重要的 细节需要注意:
#  The database 针对每个 test method 都会被重置(reset)
# The database is reset for each test method, so the first question is no longer there,
# and so again the index shouldn’t have any questions in it.
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        # https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.SimpleTestCase.assertContains
        # https://docs.djangoproject.com/en/2.2/topics/testing/tools/#django.test.TransactionTestCase.assertQuerysetEqual

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # https://docs.djangoproject.com/en/2.2/intro/tutorial05/#testing-our-new-view
    # 一个很重要的 细节需要注意:
    #  The database 针对每个 test method 都会被重置(reset)
    # The database is reset for each test method, so the first question is no longer there,
    # and so again the index shouldn’t have any questions in it.
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


# https://docs.djangoproject.com/en/2.2/intro/tutorial05/#testing-the-detailview
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
