import pytest

from unittest.mock import MagicMock

from app.dao.model.director import Director
from app.dao.director import DirectorDAO
from app.service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    nolan = Director(id=1, name='Кристофер Нолан')
    tarantino = Director(id=2, name='Квентин Тарантино')
    richi = Director(id=3, name='Гай Ричи')

    director_dao.get_one = MagicMock(return_value=nolan)
    director_dao.get_all = MagicMock(return_value=[nolan, tarantino, richi])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()
    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0

    def test_create(self):
        director_d = {
            "name": "Джеймс Ган",
        }
        director = self.director_service.create(director_d)
        assert director.id is not None

    def test_delete(self):
        self.director_service.delete(1)

    def test_update(self):
        director_d = {
            "id": 3,
            "name": "Андрей Тарковский"
        }

        self.director_service.update(director_d)