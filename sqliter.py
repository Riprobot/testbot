import psycopg2


class SQLiter:
    def __init__(self, DATABASE_URL):
        self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.connection.cursor()

    def get_players(self):
        self.cursor.execute("SELECT * FROM records "
                            "ORDER BY user_record")
        return self.cursor.fetchall()

    def player_exists(self, user_id):
        self.cursor.execute(f"SELECT * FROM records WHERE user_id = '{user_id}'")
        result = self.cursor.fetchall()
        return bool(len(result))

    def get_points(self, user_id):
        if (not self.player_exists(user_id)): return 1000000
        self.cursor.execute(f"SELECT * FROM records WHERE user_id = '{user_id}'")
        result = self.cursor.fetchall()
        return result[0][1]

    def add_player(self, user_id, points):
        return self.cursor.execute(f"INSERT INTO records (user_id,user_record) VALUES ('{user_id}',{points})")

    def update_points(self, user_id, points):
        return self.cursor.execute(f"UPDATE records SET user_record = {points} WHERE user_id = '{user_id}'")
    def commit(self):
        self.connection.commit()
    def close(self):
        self.connection.close()
