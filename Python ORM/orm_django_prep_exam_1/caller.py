import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from decimal import Decimal
from django.db.models import Q, Count, F, Case, When, Value


def populate_db():
    profile1 = Profile.objects.create(
        full_name="John Doe",
        email="john@example.com",
        phone_number="0888123456",
        address="Sofia, Bulgaria",
        is_active=True,
    )

    profile2 = Profile.objects.create(
        full_name="Maria Ivanova",
        email="maria@example.com",
        phone_number="0899123456",
        address="Plovdiv, Bulgaria",
        is_active=True,
    )

    product1 = Product.objects.create(
        name="Laptop",
        description="Fast ultrabook",
        price=Decimal("1499.99"),
        in_stock=10,
        is_available=True,
    )

    product2 = Product.objects.create(
        name="Headphones",
        description="Noise cancelling headphones",
        price=Decimal("199.99"),
        in_stock=30,
        is_available=True,
    )

    order1 = Order.objects.create(
        profile=profile1,
        total_price=Decimal("1699.98"),
        is_completed=False,
    )
    order1.products.add(product1, product2)

    order2 = Order.objects.create(
        profile=profile2,
        total_price=Decimal("199.99"),
        is_completed=True,
    )
    order2.products.add(product2)


def get_profiles(search_string=None):
    if not search_string:
        return ''

    profiles_match = Profile.objects.filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    )

    return '\n'.join(
        f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count()}"
        for p in profiles_match
    )


def get_loyal_profiles():
    return '\n'.join(
        f"Profile: {p.full_name}, orders: {p.num_of_orders}"
        for p in Profile.objects.get_regular_customers()
    )


def get_last_sold_products():
    last_order = Order.objects.last()
    if not last_order:
        return ''

    last_order_products = last_order.products.all()
    if not last_order_products:
        return ''

    return ', '.join(f"Last sold products: {p.name}" for p in last_order_products)


def get_top_products():
    top_products = (
        Product.objects.annotate(
            num_of_orders=Count('order'),
        ).filter(num_of_orders__gt=0)
        .order_by('-num_of_orders', 'name')
    )[:5]

    return f"Top products:\n" + '\n'.join(f"{p.name}, sold {p.order_set.count()} times"
                                          for p in top_products)


def apply_discounts():
    orders_to_discount = (
        Order.objects.annotate(
            num_of_orders=Count('products'),
        ).filter(num_of_orders__gt=2, is_completed=False)
        .update(total_price=F('total_price') * 0.9)
    )

    return f"Discount applied to {orders_to_discount} orders."


def complete_order():
    first_order = Order.objects.filter(is_completed=False).order_by('creation_date').first()

    if not first_order:
        return ''

    first_order.is_completed = True
    first_order.save()

    first_order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available')
        )
    )

    return "Order has been completed!"
