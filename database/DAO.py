from database.DB_connect import DBConnect
from model.nerc import Nerc
from model.powerOutages import Event


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllNerc():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * FROM Nerc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Nerc(row["id"], row["value"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEvents(nerc_id):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.id as _id, p.nerc_id as _nerc_id, p.customers_affected as _customers_affected,
		            p.date_event_began as _date_event_began, p.date_event_finished as _date_event_finished
                    FROM PowerOutages p, Nerc n
                    WHERE p.Nerc_id = n.id AND n.id = %s """

        cursor.execute(query, (nerc_id,))

        for row in cursor:
            result.append(Event(**row))

        cursor.close()
        conn.close()
        return result
"""
row["id"], row["event_type_id"],
                      row["tag_id"], row["area_id"],
                      row["nerc_id"], row["responsible_id"],
                      row["customers_affected"], row["date_event_began"],
                      row["date_event_finished"], row["demand_loss"]))"""