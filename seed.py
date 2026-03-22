from app import Yarn, db, Projects, app
from datetime import datetime

def seed_data():
    with app.app_context():

        # Seed Yarn
        if Yarn.query.count() == 0:
            yarns = [
                Yarn(y_name="Soft Cotton Blue", y_type="Cotton", y_color="Blue"),
                Yarn(y_name="Soft Cotton Red", y_type="Cotton", y_color="Red"),
                Yarn(y_name="Wool Classic Black", y_type="Wool", y_color="Black"),
                Yarn(y_name="Acrylic Bright Yellow", y_type="Acrylic", y_color="Yellow"),
                Yarn(y_name="Silk Premium White", y_type="Silk", y_color="White"),
                Yarn(y_name="Bamboo Soft Teal", y_type="Bamboo", y_color="Teal"),
                Yarn(y_name="Mixed Fiber Purple", y_type="Blend", y_color="Purple"),
                Yarn(y_name="Chunky Wool Grey", y_type="Wool", y_color="Grey"),
                Yarn(y_name="Cotton Light Pink", y_type="Cotton", y_color="Pink"),
                Yarn(y_name="Acrylic Navy", y_type="Acrylic", y_color="Navy"),
            ]

            db.session.add_all(yarns)
            db.session.commit()
            print("Yarn seed inserted")

        # Seed Projects
        if Projects.query.count() == 0:
            projects = [
                Projects(p_name="Scarf", p_due_date=datetime(2026, 4, 1).date(), p_description="Winter scarf"),
                Projects(p_name="Blanket", p_due_date=datetime(2026, 5, 10).date(), p_description="Cozy blanket"),
                Projects(p_name="Hat", p_due_date=datetime(2026, 3, 30).date(), p_description="Warm hat"),
                Projects(p_name="Gloves", p_due_date=datetime(2026, 4, 15).date(), p_description="Knitted gloves"),
                Projects(p_name="Sweater", p_due_date=datetime(2026, 6, 1).date(), p_description="Pullover sweater"),
                Projects(p_name="Socks", p_due_date=datetime(2026, 4, 20).date(), p_description="Comfort socks"),
                Projects(p_name="Bag", p_due_date=datetime(2026, 5, 5).date(), p_description="Handmade bag"),
                Projects(p_name="Shawl", p_due_date=datetime(2026, 6, 20).date(), p_description="Light shawl"),
                Projects(p_name="Toy", p_due_date=datetime(2026, 3, 25).date(), p_description="Crochet toy"),
                Projects(p_name="Table Mat", p_due_date=datetime(2026, 5, 18).date(), p_description="Decorative mat"),
            ]

            db.session.add_all(projects)
            db.session.commit()
            print("Projects seed inserted")

if __name__ == "__main__":
    seed_data()