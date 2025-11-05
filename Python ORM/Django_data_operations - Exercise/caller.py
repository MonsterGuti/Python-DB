import os
from typing import Optional

import django
from _decimal import Decimal
from django.template.backends.django import reraise
from django.utils.text import re_prt

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name, species):
    pet = Pet.objects.create(name=name, species=species)
    return f'{pet.name} is a very cute {pet.species}!'


def create_artifact(name, origin, age, description, is_magical: bool):
    artifact = Artifact.objects.create(name=name, age=age, description=description, is_magical=is_magical)
    artifact.save()
    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifatct: Artifact, new_name: str):
    if artifatct.is_magical and artifatct.age > 250:
        artifatct.name = new_name
        artifatct.save()


def delete_all_artifacts():
    artifacts = Artifact.objects.all()
    artifacts.delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    return '\n'.join(f"{l.name} has a population of {l.population}" for l in locations)


def new_capital():
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    locations = Location.objects.all()
    for location in locations:
        if location.is_capital:
            return location.name
    return None


def delete_first_location():
    first_location = Location.objects.first()
    first_location.delete()


def get_recent_cars():
    return Car.objects.all().filter(year__gte=2020).values('model', 'price_with_discount')


def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount_percent = Decimal(sum(int(digit) for digit in str(car.price)) / 100)
        discount = car.price * discount_percent
        car.price_with_discount = car.price - discount
        car.save()


def delete_last_car():
    cars = Car.objects.all()
    cars.last().delete()


def show_unfinished_tasks():
    tasks = Task.objects.all()
    message = ''
    for t in tasks:
        if not t.is_finished:
            message += f'Task - {t.title} needs to be done until {t.due_date}!\n'
    return message.strip()


def complete_odd_tasks():
    tasks = Task.objects.all()
    for t in tasks:
        if t.id % 2 == 1:
            t.is_finished = True
            t.save()


def encode_and_replace(text: str, task_title: str):
    try:
        encoded_text = ''.join(chr(ord(l) - 3) for l in text)
        for task in Task.objects.all().filter(title=task_title):
            task.description = encoded_text
            task.save()
    except Exception as e:
        print(f'Error encoding and replacing text: {e}')


def get_deluxe_room():
    deluxe_rooms = HotelRoom.objects.all().filter(room_type='deluxe')
    message = ''
    for room in deluxe_rooms:
        if room.id % 2 == 0:
            message += f'Deluxe room with number {room.room_number} costs {room.price_per_night}$ per night!'
    return message.strip()


def increase_room_capacity():
    reserved_rooms = HotelRoom.objects.all().filter(is_reserved=True).order_by('id')
    previous_room: Optional[HotelRoom] = None
    for room in reserved_rooms:
        if previous_room:
            room.capacity += previous_room.capacity
        else:
            room.capacity += room.id
        previous_room = room
        room.save()


def reserve_first_room():
    HotelRoom.objects.all().filter(is_reserved=False).update(is_reserved=True)


def delete_last_room():
    HotelRoom.objects.all().filter(is_reserved=False).order_by('-id').delete()


def update_characters():
    characters = Character.objects.all()
    for c in characters:
        if c.class_name == "Mage":
            c.level += 3
            c.intelligence = max(0, c.intelligence - 7)
        elif c.class_name == "Warrior":
            c.hit_points = c.hit_points // 2
            c.dexterity += 4
        elif c.class_name in ["Assassin", "Scout"]:
            c.inventory = "The inventory is empty"
        c.save()


def fuse_characters(first_character: Character, second_character: Character):
    new_name = f"{first_character.name} {second_character.name}"
    new_class = "Fusion"
    new_level = (first_character.level + second_character.level) // 2
    new_strength = int((first_character.strength + second_character.strength) * 1.2)
    new_dexterity = int((first_character.dexterity + second_character.dexterity) * 1.4)
    new_intelligence = int((first_character.intelligence + second_character.intelligence) * 1.5)
    new_hit_points = first_character.hit_points + second_character.hit_points

    if first_character.class_name in ["Mage", "Scout"]:
        new_inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    else:
        new_inventory = "Dragon Scale Armor, Excalibur"
    first_character.delete()
    second_character.delete()

    Character.objects.create(
        name=new_name,
        class_name=new_class,
        level=new_level,
        strength=new_strength,
        dexterity=new_dexterity,
        intelligence=new_intelligence,
        hit_points=new_hit_points,
        inventory=new_inventory,
    )


def grand_dexterity():
    Character.objects.all().update(dexterity=30)


def grand_intelligence():
    Character.objects.all().update(intelligence=40)


def grand_strength():
    Character.objects.all().update(strength=50)


def delete_characters():
    Character.objects.filter(inventory="The inventory is empty").delete()

# if __name__ == '__main__':
