from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import CustomUser
from blog.models import Category, Post

category_list = [
    "Technology",
    "Health",
    "Travel",
    "Food",
]


class Command(BaseCommand):
    help = "Generate fake data for CustomUser model"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        """Initialize the command with custom stdout and stderr."""
        super(Command, self).__init__(stdout, stderr, no_color, force_color)
        self.fake = Faker()

    def handle(self, *args, **kwargs):
        user = CustomUser.objects.create_user(
            email=self.fake.email(),
            phone=self.fake.phone_number(),
            password=self.fake.password(),
            is_verified=True,
            is_staff=False,
        )
        profile = user.profile
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.text()
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(
                name=name
            )  # get_or_create will not create duplicate categories

        for _ in range(10):
            post = Post.objects.create(
                author=profile,
                title=self.fake.sentence(),
                content=self.fake.text(),
                status=True,
                category=Category.objects.get(
                    name=self.fake.random_element(elements=category_list)
                ),
            )
            self.stdout.write(self.style.SUCCESS(f"Created Post: {post.title}"))
