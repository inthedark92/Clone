import os
import glob

def clean():
    # Delete db.sqlite3
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')
        print("Удален db.sqlite3")

    # Delete migration files
    migration_files = glob.glob('apps/*/migrations/00*.py')
    for f in migration_files:
        os.remove(f)
        print(f"Удален {f}")

if __name__ == "__main__":
    clean()
