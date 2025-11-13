from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class VipperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(Assassin):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(VengeanceDemonHunter):
    felblade_ability = models.CharField(max_length=100)


class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField()


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True

    def reply_to_message(self, reply_content: str):
        sender = self.receiver
        receiver = self.sender
        new_message = Message(sender=sender, receiver=receiver, content=reply_content)
        new_message.save()
        return new_message

    def forward_message(self, receiver: UserProfile):
        sender = self.receiver
        content = self.content
        new_message = Message(sender=sender, receiver=receiver, content=content)
        new_message.save()
        return new_message


class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value):
        if value is None:
            return None
        try:
            value_int = int(float(value))
        except (ValueError, TypeError):
            raise ValueError('Invalid input for student ID')
        return value_int

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return None
        try:
            if not isinstance(value, str):
                raise TypeError("The card number must be a string")
            if not value.isdigit():
                raise ValueError("The card number must contain only digits")
            if len(value) != 16:
                raise ValueError("The card number must be exactly 16 characters long")
            return f'****-****-****-{value[-4:]}'
        except (ValueError, TypeError) as e:
            raise ValidationError(e)


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"Room {self.number} created successfully"

    def __str__(self):
        return f"Room {self.number}"


class BaseReservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        abstract = True

    def reservation_period(self):
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self):
        total = self.room.price_per_night * self.reservation_period()
        return round(float(total), 2)


class RegularReservation(BaseReservation):

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        existing = RegularReservation.objects.filter(room=self.room)

        for r in existing:
            if not (self.end_date <= r.start_date or self.start_date >= r.end_date):
                raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        existing = SpecialReservation.objects.filter(room=self.room)

        for r in existing:
            if not (self.end_date <= r.start_date or self.start_date >= r.end_date):
                raise ValidationError(f"Room {self.room.number} cannot be reserved")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int):
        if days <= 0:
            raise ValidationError("Error during extending reservation")

        new_end_date = self.end_date + timedelta(days=days)
        existing = SpecialReservation.objects.filter(room=self.room).exclude(id=self.id)

        for r in existing:
            if not (new_end_date <= r.start_date or self.start_date >= r.end_date):
                raise ValidationError("Error during extending reservation")

        self.end_date = new_end_date
        self.save()
        return f"Extended reservation for room {self.room.number} with {days} days"


