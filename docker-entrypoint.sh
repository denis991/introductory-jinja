#!/bin/bash
set -e

# Wait for database to be ready
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready!"

# Check if tables exist by trying to query the users table
echo "Checking if database tables exist..."
python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://postgres:password@db:5432/jinja_app')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(f'Database tables exist, found {count} users')
except psycopg2.OperationalError as e:
    if 'relation \"users\" does not exist' in str(e):
        print('Database tables do not exist, will initialize')
        exit(1)
    else:
        print(f'Database connection error: {e}')
        exit(1)
except Exception as e:
    print(f'Unexpected error: {e}')
    exit(1)
" || {
    echo "Initializing database tables..."
    flask init-db
    echo "Seeding database with test data..."
    flask seed-db
    echo "Database initialized and seeded!"
}

# Start the application
echo "Starting Flask application..."
exec python run.py

# Теперь давайте также убедимся, что файл docker-entrypoint.sh имеет правильные права на выполнение локально:
# Теперь давайте проверим права на файл:
# ls -la docker-entrypoint.sh
