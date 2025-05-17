import os
from dotenv import load_dotenv
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from django.urls import reverse
from django.conf import settings
from orders.models import Order
from profiles.models import Profile
from datetime import datetime
import json

load_dotenv()

class GigaChatAssistant:
    def __init__(self):
        gigachat_credentials = os.getenv('GIGACHAT_CREDENTIALS')
        if not gigachat_credentials:
            raise ValueError("GIGACHAT_CREDENTIALS не найден в переменных окружения")
        
        self.chat = GigaChat(
            model="GigaChat-Pro",
            credentials=gigachat_credentials,
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False,
            temperature=0.7,
            top_p=0.9,
            profanity_check=True
        )
        
        self.base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        
        self.system_prompt = """
Ты профессиональный AI-ассистент фриланс-платформы. Твоя задача - помогать пользователям в строго рабочих вопросах, связанных с фрилансом, сохраняя дружелюбный и профессиональный тон.

СТРОГИЕ ПРАВИЛА ФОРМАТИРОВАНИЯ:
1. При выводе заказов:
   • Только в формате: <a href="URL" class="red-link">Название</a> (Категория: X, Бюджет: Y ₽, Срок: Z дней)
   • Бюджет всегда в рублях (₽)
   • Срок всегда в днях
   • Максимум 5 заказов

2. При выводе исполнителей:
   • Только в формате: <a href="URL" class="red-link">Имя</a> (Рейтинг: X, Навыки: Y)
   • Рейтинг указывать с точностью до десятых
   • Навыки перечислять через запятую (первые 3 основных)
   • Максимум 5 исполнителей

3. Общие правила:
   • Всегда используй точный HTML-формат ссылок как указано выше
   • Никогда не изменяй структуру ссылок
   • Если данных нет - сообщи об этом вежливо
   • Отвечай только на рабочие темы фриланса
   • На нерабочие темы вежливо отказывайся

ПРИМЕРЫ КОРРЕКТНЫХ ОТВЕТОВ:
1. Поиск заказов:
Вот подходящие заказы:
• <a class="red-link" href="https://site.com/order/1" class="order-link">Разработка логотипа</a> (Категория: Дизайн, Бюджет: 5000 ₽, Срок: 3 дня)
• <a class="red-link" href="https://site.com/order/2" class="order-link">Создание сайта-визитки</a> (Категория: Веб-разработка, Бюджет: 15000 ₽, Срок: 7 дней)

2. Поиск исполнителей:
Вот подходящие исполнители:
• <a class="red-link" href="https://site.com/profile/1" class="profile-link">Иван Петров</a> (Рейтинг: 4.8, Навыки: Python, Django, PostgreSQL)
• <a class="red-link" href="https://site.com/profile/2" class="profile-link">Анна Сидорова</a> (Рейтинг: 5.0, Навыки: Графический дизайн, Illustrator, Брендинг)

3. Общие вопросы:
На вопрос "Как составить ТЗ?" отвечай кратко и по делу, например:
Для составления ТЗ укажите: 1) Цель проекта 2) Требования 3) Сроки 4) Бюджет 5) Примеры аналогичных работ. Будьте конкретны.

4. Нерабочие темы:
На вопрос "Расскажи анекдот" отвечай:
Извините, я помогаю только с вопросами, связанными с фрилансом и работой на платформе.
"""

    def _get_orders_data(self, query=None):
        try:
            queryset = Order.objects.all()
            if query:
                queryset = queryset.filter(description__icontains=query)
            return [{
                'id': o.id,
                'title': o.title,
                'description': o.description,
                'category': o.get_category_display(),
                'budget': o.budget or "Договорная",
                'days': o.days_to_complete,
                'url': f"{self.base_url}{reverse('order_detail', kwargs={'order_id': o.id})}"
            } for o in queryset]
        except Exception as e:
            print(f"Ошибка при получении заказов: {str(e)}")
            return []

    def _get_profiles_data(self, query=None):
        try:
            queryset = Profile.objects.filter(user__is_executor=True)
            if query:
                queryset = queryset.filter(skills__icontains=query)
            return [{
                'id': p.user.id,
                'name': p.user.name,
                'skills': p.skills,
                'rating': p.user.executor.rating,
                'url': f"{self.base_url}{reverse('profiles:user_profile', kwargs={'user_id': p.user.id})}"
            } for p in queryset]
        except Exception as e:
            print(f"Ошибка при получении профилей: {str(e)}")
            return []

    def get_response(self, user_message):
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=json.dumps({
                    "system_data": {
                        "orders": self._get_orders_data(),
                        "profiles": self._get_profiles_data(),
                        "timestamp": datetime.now().isoformat()
                    },
                    "user_query": user_message
                }, ensure_ascii=False))
            ]
            
            response = self.chat.invoke(messages)
            return response.content
            
        except Exception as e:
            print(f"Ошибка GigaChat: {str(e)}")
            return "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."