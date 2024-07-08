from sqlalchemy import select

from fastapi_project.models import User


def test_create_user(session):
    user = User(
        username='enzogarcia',
        email='enzo@email.com',
        password='senha_1234',
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'enzo@email.com'))

    assert result.username == 'enzogarcia'
