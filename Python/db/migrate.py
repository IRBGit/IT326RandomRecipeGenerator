from database_operations import ServiceContainer

if __name__ == "__main__":
    container = ServiceContainer()
    container.migrate_database()