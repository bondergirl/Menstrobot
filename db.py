import sqlite3


class BotDB:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.result = False
        self.con = sqlite3.connect(self.table_name)
        self.cur = self.con.cursor()

    def db_register(self, user_id: str, username: str, now: str) -> bool:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                                        id TEXT UNIQUE NOT NULL, 
                                                        user TEXT NOT NULL,
                                                        registered TEXT NOT NULL
                                                        );
                    """)

        try:
            sqlite_insert = """INSERT
                                            INTO users (id, user, registered) 
                                            VALUES (?, ?, ?);
                            """

            user = (user_id, username, now)
            self.cur.execute(sqlite_insert, user)
            self.result = True
        except sqlite3.Error as e:
            print(repr(e))
        finally:
            self.con.commit()
            self.cur.close()
            self.con.close()
            return self.result

    def db_add_cycle(self, user_id: str, date: str) -> bool:
        self.cur.execute("""CREATE TABLE IF NOT EXISTS cycles(
                                                        id TEXT NOT NULL, 
                                                        date TEXT NOT NULL,
                                                        UNIQUE (id, date)
                                                        );
                    """)
        try:

            sqlite_insert = """INSERT 
                                        INTO cycles(id, date)
                                        VALUES (?, ?);
                            """
            cycle = (user_id, date)
            self.cur.execute(sqlite_insert, cycle)
            self.result = True
        except sqlite3.Error as e:
            print(repr(e))
        finally:
            self.con.commit()
            self.cur.close()
            self.con.close()
            return self.result

    def db_statistics(self, user_id: list) -> list:
        try:
            sql_select = """SELECT date
                                    FROM cycles
                                    WHERE id = ?;
                                    """
            self.cur.execute(sql_select, user_id)
            self.result = self.cur.fetchall()
        except sqlite3.Error as e:
            print(repr(e))
        finally:
            self.con.commit()
            self.cur.close()
            self.con.close()
            return self.result

    def db_remove_cycle(self, user_id: str, date_to_delete: str):
        try:
            sql_delete = """DELETE FROM cycles
                            WHERE id = ? AND date = ?;
                            """
            sql_data = (user_id, date_to_delete)
            self.cur.execute(sql_delete, sql_data)
            self.result = True
        except sqlite3.Error as e:
            print(repr(e))
        finally:
            self.con.commit()
            self.cur.close()
            self.con.close()
            return self.result

    def db_show_last_cycle(self, user_id: list) -> list:
        try:
            sql_select = """SELECT date
                                    FROM cycles
                                    WHERE id = ?
                                    ORDER BY date DESC
                                    LIMIT 1;
                            """
            self.cur.execute(sql_select, user_id)
            self.result = self.cur.fetchall()
            return self.result
        except sqlite3.Error as e:
            print(repr(e))
        finally:
            self.con.commit()
            self.cur.close()
            self.con.close()
