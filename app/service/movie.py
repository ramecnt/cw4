from sqlalchemy import desc

from app.dao.movie import MovieDAO



class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters):
        if filters.get("director_id") is not None:
            movies = self.dao.get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(filters.get("director_id"))
        elif filters.get("year") is not None:
            movies = self.dao.get_by_year(filters.get("director_id"))
        else:
            movies = self.dao.get_all()
        if filters.get("status") is not None and filters.get("status") == "new":
            movies = movies.order_by(desc(self.dao.get_class().year))
        if filters.get("page") is not None:
            movies = movies.limit(12).offset((int(filters.get('page')) - 1) * 12)
        return movies

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        self.dao.update(movie_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
