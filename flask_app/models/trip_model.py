from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User

db = 'trip_db'

class Trip:
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.description = data['description']
        self.from_date = data['from_date']
        self.to_date = data['to_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.planner = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM trips"
        results = connectToMySQL(db).query_db(query)
        # print(results)
        trips = []
        for trip in results:
            trips.append(cls(trip))
        return trips

    @classmethod
    def create_trip(cls, data):
        query = """
                INSERT INTO trips ( destination, description, from_date, to_date, user_id )
                VALUES ( %(destination)s, %(description)s, %(from_date)s,  %(to_date)s,  %(user_id)s );
                """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM trips WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_all_created_trips(cls):
        query = """
                SELECT * from users
                LEFT JOIN trips
                ON trips.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        print(results)
        trips = []
        for trip in results:
            planner = User(trip)
            trip_data = {
                'id' : trip['trips.id'],
                'destination' : trip['destination'],
                'description' : trip['description'],
                'from_date' : trip['from_date'],
                'to_date' : trip['to_date'],
                'created_at' : trip['created_at'],
                'updated_at' : trip['updated_at'],
                'user_id' : trip['user_id']
            }
            planner.trip = Trip(trip_data)
            trips.append(planner)
        return trips

    @classmethod
    def get_trips(cls, data):
        query = """
                SELECT * FROM trips
                JOIN users
                ON trips.user_id = users.id
                WHERE trips.id = %(id)s;
                """
        results = connectToMySQL(db).query_db(query, data)
        trip = cls(results[0])
        for row in results:
            user_data = {
                'id' : row['id'],
                'name' : row['name'],
                'user_name' : row['user_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']
            }
        trip.planner = User(user_data)
        return trip