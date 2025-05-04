import base64
import json
import re
import logging
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.models import Executor
from gigachat import GigaChat
from dotenv import load_dotenv

load_dotenv()  

logger = logging.getLogger(__name__)

GIGACHAT_CREDENTIALS = base64.b64encode(os.getenv("GIGACHAT_TOKEN").encode()).decode()
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"

def ai_find_executor(request):
    if request.method != 'POST':
        logger.warning('Invalid request method', extra={'method': request.method})
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
    try:
        logger.info('Starting executor search processing')

        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            logger.debug('Received JSON data', extra={'data': data})
        except json.JSONDecodeError:
            user_message = request.POST.get('message')
            logger.debug('Received form data', extra={'post_data': dict(request.POST)})
        
        if not user_message:
            logger.error('Empty message received')
            return JsonResponse({'error': 'Message is required'}, status=400)
        
        logger.info('Processing message', extra={'message': user_message[:100]})

        executors = Executor.objects.select_related('user', 'user__profile').all()
        logger.info(f'Found {len(executors)} executors in database')
        
        executors_info = []
        for executor in executors:
            try:
                profile = executor.user.profile

                executors_info.append({
                    'name': str(executor),
                    'skills': profile.skills if profile.skills else 'Не указано',
                    'rating': executor.rating,
                    'completed_orders': executor.completed_orders,
                    'id': executor.user.id
                })
            except Exception as e:
                logger.error(f'Error processing executor {executor.id}', exc_info=True)
                continue

        logger.debug('Prepared executors info', extra={'executors_info': executors_info[:2]})

        

        prompt = f"""
               1. Анализируй запрос клиента ТОЛЬКО на предмет:
            - Описания конкретной задачи/услуги (например: "Нужен дизайнер логотипа")
            - Профессиональных навыков (например: "Ищу программиста Python")
            - Четких требований к исполнителю

            2. Если запрос:
            - Является приветствием/прощанием
            - Не содержит профессионального запроса
            - Содержит абстрактные фразы без конкретики
            - Не относится к поиску исполнителей
            — отвечай СТРОГО: "Исполнители не найдены!"

            3. Для корректных запросов:
            - Выбери ОДНОГО наиболее подходящего исполнителя
            - Если ни один не подходит — ответ "Исполнители не найдены!"
            - Формат ответа СТРОГО такой:
            "Согласно вашим требованиям вам подходит этот исполнитель - [Имя пользователя]. [Одна краткая причина выбора]. <a href='http://127.0.0.1:8000/profiles/[id пользователя]/' target='_blank' class='profile-link'>Ссылка на профиль</a>"
            - В ответе ДОЛЖНА быть ссылка в указанном формате с '/' в конце!

            4. НЕ показывай:
            - Свои рассуждения
            - Анализ других исполнителей
            - Любую дополнительную информацию

            Запрос клиента: "{user_message}"
            Доступные исполнители: {json.dumps(executors_info, ensure_ascii=False)}

            Ответь СТРОГО в указанном формате без лишних слов!

        """
        
        logger.debug('Prepared prompt for AI', extra={'prompt': prompt[:500]})

        try:
            logger.info('Sending request to GigaChat API')
            
            giga = GigaChat(
                credentials=GIGACHAT_CREDENTIALS,
                scope=GIGACHAT_SCOPE,
                verify_ssl_certs=False,
                model="GigaChat:latest",
            )
            
            response = giga.chat(prompt)
            
            giga.close()
                
            if not response or not hasattr(response, 'choices') or not response.choices:
                logger.error('Invalid API response structure')
                return JsonResponse({'error': 'Invalid API response'}, status=503)
            
            logger.debug('Received API response', extra={
                'api_response': str(response),
                'model': getattr(response, 'model', None)
            })
            
            ai_response = response.choices[0].message.content
            logger.info('Successfully received AI response', extra={'response': ai_response})
            
            if not re.search(r"Согласно вашим требованиям вам подходит этот исполнитель - .*?<a href='http://127\.0\.0\.1:8000/profiles/\d+/'", ai_response):
                if "Исполнители не найдены!" not in ai_response:
                    logger.warning('AI response format is incorrect, forcing default response')
                    ai_response = "Исполнители не найдены!"
            
            from django.utils.safestring import mark_safe
            return JsonResponse({'response': mark_safe(ai_response)})
            
        except Exception as e:
            logger.error('GigaChat API request failed', exc_info=True)
            return JsonResponse({
                'error': 'AI service unavailable',
                'details': str(e),
                'type': type(e).__name__
            }, status=503)
    
    except Exception as e:
        logger.critical('Unexpected error in ai_find_executor', exc_info=True)
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e),
            'type': type(e).__name__
        }, status=500)