import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import RegularRestaurantReview, Restaurant, MenuReview, Menu

Restaurant.objects.create(name="Savory Delight", location="456 Elm Avenue", rating=4.2,)
restaurant_from_db = Restaurant.objects.get(name="Savory Delight")
RegularRestaurantReview.objects.create(reviewer_name="Alice", restaurant=restaurant_from_db, rating=4, review_content="Good experience overall.")
review_from_db = RegularRestaurantReview.objects.get(reviewer_name="Alice", restaurant=restaurant_from_db)
print(
    f"Reviewer name: {review_from_db.reviewer_name}\n"
    f"Restaurant: {review_from_db.restaurant.name}\n"
    f"Rating: {review_from_db.rating}\n"
    f"Review content: {review_from_db.review_content}"
)

Menu.objects.create(name="Delightful Food Menu", description="Appetizers:\nSpinach and Artichoke Dip\nMain Course:\nGrilled Salmon\nDesserts:\nChocolate Fondue", restaurant=restaurant_from_db)
menu_from_db = Menu.objects.get(name="Delightful Food Menu")
MenuReview.objects.create(reviewer_name="Lilly", menu=menu_from_db, rating=5, review_content="Delicious food")
menu_review_from_db = MenuReview.objects.get(reviewer_name="Lilly", menu=menu_from_db)
print(
    f"Reviewer name: {menu_review_from_db.reviewer_name}\n"
    f"Menu: {menu_review_from_db.menu.name}\n"
    f"Rating: {menu_review_from_db.rating}\n"
    f"Review content: {menu_review_from_db.review_content}"
)
