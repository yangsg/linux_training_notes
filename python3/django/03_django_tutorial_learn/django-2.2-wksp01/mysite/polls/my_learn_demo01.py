'''
该示例来自: Playing with the API
    https://docs.djangoproject.com/en/2.2/intro/tutorial02/#playing-with-the-api
'''

from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
Question.objects.all()
## <QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
from django.utils import timezone

q = Question(question_text="What's new?", pub_date=timezone.now())  # <--- 注:这里使用的是 timezone.now(),因为启用了时区支持

# Save the object into the database. You have to call save() explicitly.
q.save()

# Now it has an ID.
q.id
## 1

# Access model field values via Python attributes.
q.question_text
## "What's new?"
q.pub_date
## datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
q.question_text = "What's up?"
q.save()

# objects.all() displays all the questions in the database.
Question.objects.all()
## <QuerySet [<Question: Question object (1)>]>


'''
mysql> select * from polls_question;
+----+---------------+----------------------------+
| id | question_text | pub_date                   |
+----+---------------+----------------------------+
|  1 | What's up?    | 2019-08-04 07:22:19.276409 |
+----+---------------+----------------------------+
'''

