import os
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import telegram
from .models import Habit


@shared_task
def send_telegram_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        if not habit.user.telegram_chat_id:
            return f"Пользователь {habit.user.username} не настроил Telegram"
        
        bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
        
        message = f"🔔 Напоминание о привычке!\n\n"
        message += f"Время выполнить: {habit.action}\n"
        message += f"Место: {habit.place}\n"
        message += f"Время: {habit.time}\n"
        message += f"Время на выполнение: {habit.execution_time} секунд\n"
        
        if habit.reward:
            message += f"Вознаграждение: {habit.reward}\n"
        elif habit.related_habit:
            message += f"Связанная привычка: {habit.related_habit.action}\n"
        
        bot.send_message(chat_id=habit.user.telegram_chat_id, text=message)
        return f"Напоминание отправлено для привычки {habit.id}"
        
    except Habit.DoesNotExist:
        return f"Привычка {habit_id} не найдена"
    except Exception as e:
        return f"Ошибка отправки напоминания: {str(e)}"


@shared_task
def check_and_send_reminders():
    now = timezone.now()
    current_time = now.time()
    
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    )
    
    for habit in habits:
        last_log = habit.habitlog_set.order_by('-completed_at').first()
        
        if not last_log:
            send_telegram_reminder.delay(habit.id)
            continue
        
        days_since_last = (now.date() - last_log.completed_at.date()).days
        
        if days_since_last >= habit.periodicity:
            send_telegram_reminder.delay(habit.id)
    
    return f"Проверено {habits.count()} привычек" 