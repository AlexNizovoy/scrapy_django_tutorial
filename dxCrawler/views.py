from uuid import uuid4
from user_agent import generate_user_agent
from scrapyd_api import ScrapydAPI
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800')


@require_http_methods(['POST', 'GET'])
def crawl(request):
    if request.method == 'POST':
        unique_id = str(uuid4())
        settings = {
            'uunique_id': unique_id,
            'USER_AGENT': generate_user_agent(os=('linux', 'mac'), device_type='desktop')
        }

        task = scrapyd.schedule('scrapy_app', 'nbu_crawler', settings=settings)

        return JsonResponse({
            'task_id': task,
            'unique_id': unique_id,
            'status': 'started',
        })

    elif request.method == 'GET':
        task_id = request.GET.get('task_id', None)
        unique_id = request.GET.get('unique_id', None)
        if not task_id or not unique_id:
            return JsonResponse({'error': 'Missing args'})

        status = scrapyd.job_status('scrapy_app', task_id)
        if status == 'finished':
            pass
        else:
            return JsonResponse({'status': status})
