banner.connection.Connection(self, host, user, passwd=None, db=None, ssl_key=None, ssl_cert=None, name=None):
    - Create connection object compatible with banner.queries  
    - **raises MySQLError for bad connection**

banner.connection.connections(conns: Dict[str, Connection] = {}):
    - Getter/Setter for known connections dict

banner.simple_query(query: str, connection=None, as_df=True) -> pd.DataFrame:
    - run a simple string query for connection
    - return data as list of dicts / df (as_df) 
    - connection=None try to get first known connection, **raise KeyError if None found**

banner.queries.neware_query(device: int, unit: int, channel: int, test: int, connection: Union[Connection, str] = None, raw=False):
    - query connection for device, unit, channel, test 
    - connection=None try to get first known connection, **raise KeyError if None found**
    - raw=True return data as saved in the db
    - raw=False compute temp, voltage, current aswell as grouping by auxchl_id
    - **raises Type err if no data exists**

banner.queries.neware_query_by_test(table: str, cell: int, test: int, connection: Union[Connection, str] = None, raw=False):
    - query connection for device, unit, channel, test, as well as the connection storing the data,
    - connection=None try to get first known connection, **raise KeyError if None found**
    - returns neware_query for result values, **the connection has to be an entry in connections()**
    - **raises Type err if no data exists**
    

banner.queries.describe_table(table, connection: Union[Connection, str] = None)
    - Returns a series of table columns
    - connection=None try to get first known connection, **raise KeyError if None found**

banner.queries.describe(table, connection: Union[Connection, str] = None)
    - Returns a series of db tables
    - connection=None try to get first known connection, **raise KeyError if None found**
