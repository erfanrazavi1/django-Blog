import pytest
from comments.models import Comment
from blog.models import Post
from accounts.models import CustomUser


@pytest.mark.django_db
def test_create_comment():
    user = CustomUser.objects.create_user(
        email="test@example.com", phone="09173437848", password="12345678"
    )

    post = Post.objects.create(
        title="Test Post",
        content="Some content here",
        author=user.profile,
        category=None,
        status=True,
    )

    comment = Comment.objects.create(
        user=user, post=post, content="This is a test comment"
    )

    assert comment.user == user
    assert comment.post == post
    assert comment.content == "This is a test comment"
    assert comment.parent is None
    assert comment.is_active is True
    assert comment.created_at is not None


@pytest.mark.django_db
def test_reply_to_comment():
    user = CustomUser.objects.create_user(
        email="reply@example.com", phone="09176578753", password="12345678"
    )
    post = Post.objects.create(
        title="Reply Post",
        content="...",
        author=user.profile,
        category=None,
        status=True,
    )

    parent_comment = Comment.objects.create(
        user=user, post=post, content="Parent comment"
    )
    child_comment = Comment.objects.create(
        user=user, post=post, content="Child comment", parent=parent_comment
    )

    assert child_comment.parent == parent_comment
    assert parent_comment.replies.count() == 1
