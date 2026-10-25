from django.db import models
from django.contrib.auth.models import User


class Advert(models.Model):
    title = models.CharField("Название ролика", max_length=200)
    customer = models.CharField("Заказчик", max_length=200)
    program = models.CharField("Передача", max_length=200)
    rating = models.DecimalField("Рейтинг передачи", max_digits=10, decimal_places=2)
    air_date = models.DateField("Дата эфира")
    duration = models.IntegerField("Длительность, сек")
    minute_price = models.DecimalField("Стоимость минуты, руб.", max_digits=10, decimal_places=2)
    agent = models.CharField("Агент", max_length=200)
    agent_percent = models.DecimalField("Процент агента, %", max_digits=10, decimal_places=2)
    text = models.TextField("Сведения о заказчике")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор записи")
    created_date = models.DateField("Дата создания записи", auto_now_add=True)

    class Meta:
        verbose_name = "рекламный ролик"
        verbose_name_plural = "Рекламные ролики"

    def __str__(self):
        return "%s: %s" % (self.customer, self.title)

    def get_excerpt(self):
        return self.text[:140] + "..." if len(self.text) > 140 else self.text

    def get_cost(self):
        # стоимость рекламы = длительность ролика в минутах * стоимость минуты
        return round(self.duration * self.minute_price / 60, 2)

    def get_agent_salary(self):
        # зарплата агента - процент от стоимости рекламы, прошедшей в эфире
        return round(self.get_cost() * self.agent_percent / 100, 2)
