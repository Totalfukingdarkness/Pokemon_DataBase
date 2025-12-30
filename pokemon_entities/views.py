import folium

from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from .models import Pokemon, PokemonEntity


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def get_image_url(request, pokemon):
    if pokemon.image:
        return request.build_absolute_uri(pokemon.image.url)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    time_now = timezone.localtime()
    pokemons = PokemonEntity.objects.filter(appeared_at__lte=time_now,
                                            disappeared_at__gte=time_now)
    for pokemon in pokemons:
        add_pokemon(
            folium_map, pokemon.lat,
            pokemon.lon,
            get_image_url(request, pokemon.pokemon)
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image_url = get_image_url(request, pokemon)
        pokemons_on_page.append({
            'pokemon_id': pokemon.pk,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    time_now = timezone.localtime()
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    previous_evolution = {}
    if pokemon.previous_evolution:
        previous_evolution = {
            'title_ru': pokemon.previous_evolution.title,
            'pokemon_id': pokemon.previous_evolution.id,
            'img_url': get_image_url(request, pokemon.previous_evolution),
            }

    next_pokemon = pokemon.next_evolutions.first()
    next_evolution = {}
    if next_pokemon:
        next_evolution = {
            "title_ru": next_pokemon.title_ru,
            "pokemon_id": next_pokemon.id,
            "img_url": get_image_url(request, next_pokemon),
        }

    pokemon_data = {
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        "img_url": get_image_url(request, pokemon),
        'description': pokemon.description,
        'previous_evolution': previous_evolution,
        'next_evolution': next_evolution
    }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entitys = PokemonEntity.objects.filter(pokemon=pokemon,
                                                   appeared_at__lte=time_now,
                                                   disappeared_at__gte=time_now)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            get_image_url(request, pokemon_entity.pokemon)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
