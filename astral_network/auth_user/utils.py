def get_connection_code(first_name, last_name):
    return abs(hash(first_name) + hash(last_name))