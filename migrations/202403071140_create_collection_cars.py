from mongodb_migrations.base import BaseMigration


class Migration(BaseMigration):
    def upgrade(self):
        self.db.create_collection("cars")

    def downgrade(self):
        self.db.drop_collection("cars")
