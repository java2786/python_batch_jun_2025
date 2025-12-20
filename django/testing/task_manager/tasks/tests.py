from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task


class TaskModelTest(TestCase):
    # dummy task create
    def setUp(self):
        # print("setup ************")
        self.user = User.objects.create(username="demo", password="demo@123")
        self.task = Task.objects.create(
            user = self.user,
            title = "Testing Task 1",
            description = "this is a task description to test.",
            status = 'completed'
        )
        return super().setUp()
    
    def test_demo(self):
        # print("demo ************")
        # self.assertEqual(4,48)
        self.assertEqual("Testing Task 1", self.task.title)
        self.assertIn("this", self.task.description)
        self.assertIn("task description", self.task.description)
        self.assertIn("to test", self.task.description)
        self.assertIn("this is a task description to test", self.task.description)
        self.assertEqual("Completed".lower(), self.task.status.lower())
    
    def test_absolute_url(self):
        self.assertEqual(f"/tasks/{self.task.pk}/", self.task.get_absolute_url())