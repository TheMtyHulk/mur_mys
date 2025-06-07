def parse_pg_conn_str(conn_str):
    parts = conn_str.split()
    conn_dict = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            conn_dict[key] = value
    return conn_dict