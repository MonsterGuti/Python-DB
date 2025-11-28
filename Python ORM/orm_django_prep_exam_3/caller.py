import os
import django
from django.db.models import Q, F, Min, Avg, Max

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import *


def get_houses(search_string=None):
    if not search_string:
        return "No houses match your search."

    houses = House.objects.filter(
        Q(name__startswith=search_string) | Q(motto__startswith=search_string)
    )

    if not houses.exists():
        return "No houses match your search."

    result = []

    for h in houses:
        motto = h.motto if h.motto else "N/A"
        result.append(f"House: {h.name}, wins: {h.wins}, motto: {motto}")

    return result


def get_most_dangerous_house():
    dangerous_house = House.objects.annotate(
        total_dragons=Count('dragon'),
    ).order_by('-total_dragons', 'name').first()

    if not dangerous_house:
        return "No relevant data."

    ruling_status = "ruling" if dangerous_house.is_ruling else "not ruling"

    return (
        f"The most dangerous house is the House of {dangerous_house.name} "
        f"with {dangerous_house.total_dragons} dragons. "
        f"Currently {ruling_status} the kingdom."
    )


def get_most_powerful_dragon():
    powerful_dragon = Dragon.objects.filter(
        is_healthy=True
    ).order_by('-power', 'name').first()

    if not powerful_dragon:
        return "No relevant data."

    return (
        f"The most powerful healthy dragon is {powerful_dragon.name}"
        f" with a power level of {powerful_dragon.power:.1f},"
        f" breath type {powerful_dragon.breath}, and {powerful_dragon.wins} wins,"
        f" coming from the house of {powerful_dragon.house.name}."
        f" Currently participating in {powerful_dragon.quest_set.count()} quests."
    )


def update_dragons_data():
    dragons_to_update = Dragon.objects.filter(
        power__gt=1.0,
        is_healthy=False
    ).update(is_healthy=True, power=F("power") - 0.1)

    if not dragons_to_update:
        return "No changes in dragons data."

    min_power = Dragon.objects.aggregate(
        min_power=Min("power")
    )['min_power']

    return (
        f"The data for {dragons_to_update} dragon/s has been changed."
        f" The minimum power level among all dragons is {min_power:.1f}"
    )


def get_earliest_quest():
    earliest_quest = Quest.objects.order_by('start_time').first()
    if not earliest_quest:
        return "No relevant data."

    day = earliest_quest.start_time.day
    month = earliest_quest.start_time.month
    year = earliest_quest.start_time.year

    dragons = earliest_quest.dragons.all().order_by('power', 'name')
    if dragons.exists():
        dragons_string = '*'.join(d.name for d in dragons)
        avg_power_level = dragons.aggregate(avg_power=Avg('power'))['avg_power']
        avg_power_level = f"{avg_power_level:.2f}"
    else:
        dragons_string = "No dragons"
        avg_power_level = "0.00"

    return (
        f"The earliest quest is: {earliest_quest.name}, code: {earliest_quest.code}, "
        f"start date: {day}.{month}.{year}, host: {earliest_quest.host.name}. "
        f"Dragons: {dragons_string}. "
        f"Average dragons power level: {avg_power_level}"
    )


def announce_quest_winner(quest_code):
    try:
        quest = Quest.objects.get(code=quest_code)
    except Quest.DoesNotExist:
        return "No such quest."

    dragons = quest.dragons.all()
    max_power = dragons.aggregate(max_power=Max('-power'))['max_power']
    winner_dragon = dragons.filter(power=max_power).order_by('name').first()

    winner_dragon.wins += 1
    winner_dragon.save()

    winner_dragon.house.wins += 1
    winner_dragon.house.save()

    quest.delete()

    return (
        f"The quest: {quest.name} has been won by dragon {winner_dragon.name} from house {winner_dragon.house.name}."
        f" The number of wins has been updated as follows: {winner_dragon.wins} total wins for the dragon"
        f" and {winner_dragon.house.wins} total wins for the house."
        f" The house was awarded with {quest.reward:.2f} coins."
    )
