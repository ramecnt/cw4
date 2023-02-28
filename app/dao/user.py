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
        user.title = user_d.get("username")
        user.description = user_d.get("password")
        user.trailer = user_d.get("role")

        self.session.add(user)
        self.session.commit()

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
