import json
import pg8000


def query(db_client, query_string):
    try:
        with db_client.cursor() as cursor:

            cursor.execute(query_string)

            return True

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()


def get_many(db_client, query_string):
    try:
        with db_client.cursor() as cursor:
            cursor.execute(query_string)

        result = cursor.fetchall()

        if result is None:
            return None

        else:
            return result

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()


def get_one(db_client, query_string):

    try:
        with db_client.cursor() as cursor:
            cursor.execute(query_string)

        result = cursor.fetchone()

        if result is None:
            return None

        else:
            return result

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()


def get_many_list(db_client, query_list):
    result_list = []
    try:
        for query in query_list:
            with db_client.cursor() as cursor:
                cursor.execute(query)
            result_list.append(cursor.fetchall())

        if () in result_list or None in result_list:
            return False
        else:
            return result_list

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()


def get_many_list_v2(db_client, query_list):
    result_list = []
    try:
        for query in query_list:

            with db_client.cursor() as cursor:
                cursor.execute(query)
            result_list.append(cursor.fetchall())

        return result_list

    except (Exception, pg8000.DatabaseError) as error:
        print(error)
        return False
    finally:
        db_client.commit()
        db_client.close()
