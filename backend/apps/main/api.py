from django.http import JsonResponse


def animals(request):
    response = JsonResponse({
        'data': [
            'Dog',
            'Cat',
            'Bird',
            'Fish',
            'Monkey',
        ]
    })
    return response
