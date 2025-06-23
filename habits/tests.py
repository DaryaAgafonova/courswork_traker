from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Habit, HabitLog
from .serializers import HabitSerializer

User = get_user_model()


class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Делать зарядку',
            execution_time=60
        )
        self.assertEqual(habit.action, 'Делать зарядку')
        self.assertEqual(habit.user, self.user)
    
    def test_habit_validation_reward_and_related_habit(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Принять ванну',
            is_pleasant=True,
            execution_time=120
        )
        
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='09:00:00',
                action='Делать зарядку',
                reward='Шоколадка',
                related_habit=pleasant_habit,
                execution_time=60
            )
            habit.full_clean()
    
    def test_habit_validation_execution_time(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='09:00:00',
                action='Делать зарядку',
                execution_time=121
            )
            habit.full_clean()
    
    def test_habit_validation_related_habit_not_pleasant(self):
        useful_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Делать зарядку',
            is_pleasant=False,
            execution_time=60
        )
        
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='10:00:00',
                action='Другая привычка',
                related_habit=useful_habit,
                execution_time=60
            )
            habit.full_clean()
    
    def test_pleasant_habit_validation(self):
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Принять ванну',
            is_pleasant=True,
            execution_time=120
        )
        
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='09:00:00',
                action='Делать зарядку',
                is_pleasant=True,
                reward='Шоколадка',
                execution_time=60
            )
            habit.full_clean()
    
    def test_habit_validation_periodicity(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place='Дом',
                time='09:00:00',
                action='Делать зарядку',
                periodicity=8,
                execution_time=60
            )
            habit.full_clean()


class HabitLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Делать зарядку',
            execution_time=60
        )
    
    def test_habit_log_creation(self):
        log = HabitLog.objects.create(habit=self.habit)
        self.assertEqual(log.habit, self.habit)
        self.assertIsNotNone(log.completed_at)


class HabitSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='10:00:00',
            action='Принять ванну',
            is_pleasant=True,
            execution_time=120
        )
    
    def test_habit_serializer_valid_data(self):
        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Делать зарядку',
            'execution_time': 60,
            'periodicity': 1
        }
        serializer = HabitSerializer(data=data)
        self.assertTrue(serializer.is_valid())
    
    def test_habit_serializer_invalid_execution_time(self):
        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Делать зарядку',
            'execution_time': 121,
            'periodicity': 1
        }
        serializer = HabitSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('execution_time', serializer.errors)


class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.habit = Habit.objects.create(
            user=self.user,
            place='Дом',
            time='09:00:00',
            action='Делать зарядку',
            execution_time=60
        )
    
    def test_get_habits_list(self):
        response = self.client.get('/api/habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_habit(self):
        data = {
            'place': 'Офис',
            'time': '10:00:00',
            'action': 'Пить воду',
            'execution_time': 30,
            'periodicity': 1
        }
        response = self.client.post('/api/habits/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 2)
    
    def test_update_habit(self):
        data = {
            'place': 'Дом',
            'time': '09:00:00',
            'action': 'Делать зарядку обновленную',
            'execution_time': 60,
            'periodicity': 1
        }
        response = self.client.put(f'/api/habits/{self.habit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, 'Делать зарядку обновленную')
    
    def test_delete_habit(self):
        response = self.client.delete(f'/api/habits/{self.habit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
    
    def test_complete_habit(self):
        response = self.client.post(f'/api/habits/{self.habit.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HabitLog.objects.count(), 1)
    
    def test_public_habits_list(self):
        self.habit.is_public = True
        self.habit.save()
        
        response = self.client.get('/api/public-habits/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 