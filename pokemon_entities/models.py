from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField('Название на русском', max_length=200)
    title_eng = models.CharField('Название на английском', max_length=200, blank=True)
    title_jp = models.CharField('Название на японском', max_length=200, blank=True)
    image = models.ImageField('Изображение', upload_to='pokemon_images', null=True, blank=True)
    description = models.TextField('Описание', blank=True)
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                            related_name="next_evolutions", verbose_name="Предыдущая эволюция")

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entities', verbose_name='Покемон')
    lat = models.FloatField('Широта', blank=True, null=True)
    lon = models.FloatField('Долгота', blank=True, null=True)
    appeared_at = models.DateTimeField('Время появления', blank=True, null=True)
    disappeared_at = models.DateTimeField('Время исчезания', blank=True, null=True)
    level = models.IntegerField('Уровень', blank=True, null=True)
    health = models.IntegerField('Здоровье', blank=True, null=True)
    strength = models.IntegerField('Атака', blank=True, null=True)
    defence = models.IntegerField('Защита', blank=True, null=True)
    stamina = models.IntegerField('Выносливость', blank=True, null=True)