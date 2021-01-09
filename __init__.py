from .obj_connection import Connection

def NewConnection(user:str, password:str, host:str, port:int) -> Connection:
    """
    NewConnection create a connection object and connect to sql server.
    """
    conn = Connection()
    conn.host = host
    conn.port = port
    conn.user = user
    conn.password = password
    conn.connect()
    return conn