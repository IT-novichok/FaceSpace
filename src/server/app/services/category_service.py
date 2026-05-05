from ..data import db, Category


def get_category(id: int) -> Category:
    return db.session.get(Category, id).first()


def get_category_by_name(name: str) -> Category:
    return db.session.query(Category).filter(Category.name == name).first()


def get_all_categories() -> list[Category]:
    return db.session.query(Category).all()
