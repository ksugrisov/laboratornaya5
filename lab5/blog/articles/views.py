from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ValidationError
from .models import Advert


def archive(request):
    return render(request, 'archive.html', {"posts": Advert.objects.all()})


def get_advert(request, advert_id):
    try:
        post = Advert.objects.get(id=advert_id)
        return render(request, 'advert.html', {"post": post})
    except Advert.DoesNotExist:
        raise Http404


def create_advert(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # в словаре form хранится информация, введенная пользователем
            form = {
                'title': request.POST["title"],
                'customer': request.POST["customer"],
                'program': request.POST["program"],
                'rating': request.POST["rating"],
                'air_date': request.POST["air_date"],
                'duration': request.POST["duration"],
                'minute_price': request.POST["minute_price"],
                'agent': request.POST["agent"],
                'agent_percent': request.POST["agent_percent"],
                'text': request.POST["text"],
            }
            required = ['title', 'customer', 'program', 'rating', 'air_date', 'duration',
                        'minute_price', 'agent', 'agent_percent', 'text']
            if all(form[name] for name in required):
                # проверка уникальности названия ролика
                if Advert.objects.filter(title=form["title"]).exists():
                    form['errors'] = "Ролик с таким названием уже существует"
                    return render(request, 'create_advert.html', {'form': form})
                try:
                    # если поля заполнены без ошибок, создается новая запись
                    advert = Advert.objects.create(
                        title=form["title"],
                        customer=form["customer"],
                        program=form["program"],
                        rating=form["rating"],
                        air_date=form["air_date"],
                        duration=form["duration"],
                        minute_price=form["minute_price"],
                        agent=form["agent"],
                        agent_percent=form["agent_percent"],
                        text=form["text"],
                        author=request.user
                    )
                except (ValueError, ValidationError):
                    form['errors'] = "Проверьте правильность чисел и дат"
                    return render(request, 'create_advert.html', {'form': form})
                # переход на страницу созданной записи
                return redirect('get_advert', advert_id=advert.id)
            else:
                # если введенные данные некорректны
                form['errors'] = "Не все поля заполнены"
                return render(request, 'create_advert.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_advert.html', {})
    else:
        raise Http404
