from django.test import TestCase

# Create your tests here.
import datetime
from django.utils import timezone
from django.urls import reverse

from .models import Question,Choice
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)
        
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(),False)
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(),True)
def create_question(question_text,days):
    time = timezone.now() +datetime.timedelta(days=days)
    qusetion = Question.objects.create(question_text=question_text,pub_date=time)
    return qusetion 
class QuestionIndexViewsTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list',[]])
    def test_past_question(self):
        create_question(question_text="past question",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question>']
        )

class PollsAppTests(TestCase):
    def setUp(self):
        self.question = Question.objects.create(text="Test Question")
        self.choice = Choice.objects.create(question=self.question, choice_text="Choice 1")
        self.choice = Choice.objects.create(question=self.question, choice_text="Choice 2")
        

    def test_index_view(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Question")

    def test_details_view(self):
        response = self.client.get(reverse('polls:details', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Question")
        self.assertContains(response, "Choice 1")

    def test_results_view(self):
        response = self.client.get(reverse('polls:results', args=(self.question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Question")
        self.assertContains(response, "Choice 2")

        
    def test_votes_view(self):
        response = self.client.post(reverse('polls:votes', args=(self.question.id,)), {'choice': self.choice.id})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        updated_choice = Choice.objects.get(id=self.choice.id)
        self.assertEqual(updated_choice.votes, 1)

    def test_add_question(self):
        response = self.client.post(reverse('polls:index'), {'text': 'New Test Question'})
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(Question.objects.filter(text='New Test Question').exists())

    def test_delete_question(self):
        response = self.client.post(reverse('polls:delete_question', args=(self.question.id,)))
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertIs(Question.objects.filter(id=self.question.id).exists(),False)

        
