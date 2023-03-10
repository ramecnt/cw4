from app.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def delete(self, bid):
        user = self.get_one(bid)
        self.session.delete(user)
        self.session.commit()

    def create(self, data):
        ent = User(**data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def update(self, user_d):
        user = self.get_one(user_d.get("id"))
        if "password" in user_d:
            user.password = user_d.get("password")
        if "name" in user_d:
            user.name = user_d.get("name")
        if "surname" in user_d:
            user.surname = user_d.get("surname")
        if "favorite_genre" in user_d:
            user.favorite_genre = user_d.get("favorite_genre")

        self.session.add(user)
        self.session.commit()

    def get_by_email(self, e_mail):
        return self.session.query(User).filter(User.e_mail == e_mail).first()
