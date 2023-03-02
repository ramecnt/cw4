import pytest

from unittest.mock import MagicMock

from app.dao.model.movie import Movie
from app.dao.movie import MovieDAO
from app.service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie1 = Movie(id=1, title='Oppenheimer',
                   description='История жизни американского физика Роберта Оппенгеймера, который стоял во главе первых разработок ядерного оружия.',
                   trailer='https://www.kinopoisk.ru/film/4664634/', year=2023, rating=10.0, genre_id=4, director_id=2)
    movie2 = Movie(id=2, title='Король и Шут',
                   description='История, как панки из Петербурга выбирали название группы, давали первые концерты, собрали полный зал «Юбилейного», впервые выступили в Москве и на крупнейших площадках страны. Параллельно истории становления группы и отношений между её участниками Горшок и Князь отправляются в сказочный мир спасать принцессу из плена колдуна. В пути они встречают персонажей, о которых поют в своих песнях.',
                   trailer='https://www.kinopoisk.ru/series/4647040/', year=2023, rating=8.3, genre_id=4, director_id=2)
    movie3 = Movie(id=3, title='Убийцы цветочной луны',
                   description='История разворачивается в 1920-х годах вокруг индейского племени осейдж, проживающего в американском городе Оклахома. Коренных жителей США убивают одного за другим после того, как один из них разбогател, обнаружив нефть. Массовые убийства осейджей привлекают внимание ФБР, и оно приступает к расследованию.',
                   trailer='https://www.kinopoisk.ru/film/1077781/', year=2023, rating=10.0, genre_id=4, director_id=2)

    movie_dao.get_one = MagicMock(return_value=movie1)
    movie_dao.get_all = MagicMock(return_value=[movie1, movie2, movie3])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()
    return movie_dao


class TestmovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_service.get_all(filters={"director_id":None,
                                                     "genre_id":None,
                                                     "year":None})

        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            "title": "Дюна 2",
            "description": "Продолжение произведения Дени Вильнёв о загадочном мире",
            "trailer": "https://www.kinopoisk.ru/film/4540126/",
            "year": 2023,
            "rating": 10.0,
            "genre_id": 4,
            "director_id": 11
        }
        movie = self.movie_service.create(movie_d)
        assert movie.id is not None

    def test_delete(self):
        self.movie_service.delete(1)

    def test_update(self):
        movie_d = {
            "title": 'Убийцы цветочной луны',
            "description": 'История разворачивается в 1920-х годах вокруг индейского племени осейдж, проживающего в американском городе Оклахома. Коренных жителей США убивают одного за другим после того, как один из них разбогател, обнаружив нефть. Массовые убийства осейджей привлекают внимание ФБР, и оно приступает к расследованию.',
            "trailer": 'https://www.kinopoisk.ru/film/1077781/', "year": 2023, "rating": 10.0, "genre_id": 4,
            "director_id": 2
        }

        self.movie_service.update(movie_d)
