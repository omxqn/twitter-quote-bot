#pip install mysql-connector-python
import mysql.connector
import datetime
global times
global date
date = datetime.datetime.now().date()
times = datetime.datetime.now().time().strftime(f'%H:%M:%S')

db = mysql.connector.connect(
    host='remotemysql.com',
    user='NdWVc90z4c',
    passwd='kWfhLl1tVk',
    database= 'NdWVc90z4c')
my_curser = db.cursor()

# Create new table
'''

# view table descriptions
my_curser.execute('DESCRIBE id_list')
for i in my_curser:
    print(i)
'''

def new_table(table_name,instractions):
    '''Create new table'''
    try:
        # UNSIGNED there is no - or +
        # Example: instractions =  mention_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50)
        my_curser.execute(f'CREATE TABLE {table_name} ({instractions})')
        return "Table has been created successfully"
    except Exception:
        return 'This table is already existed'
def add_new(table,name,id,message): # Insert new details
    '''Add new data in elements'''
    # table = id_list
    try:
        my_curser.execute(f'INSERT INTO {table} (name,id,date,message) VALUES {(name, id, str(date)+" "+str(times), message)}')
        print("committing")
        db.commit()
        print("Data saved successfully in database")
    except Exception:
        try:
            print("Message has error")
            my_curser.execute(f'INSERT INTO {table} (name,id,date) VALUES {(name, id, str(date) + " " + str(times))}')
            print("committing")
            db.commit()
            print("Data saved successfully in database")
        except Exception:
            print("Error while adding to database")


def get_table_info(table,id):
    '''Get infos of the current table'''
    try:
        my_curser.execute(f'SELECT * FROM {table}')
        if id == True:
            x = []
            for i in my_curser:
                x.append(i[2])
            print("Data imported successfully")
            return x
        else:
            x = []
            for i in my_curser:
                x.append(i)
            print("Data imported successfully")
            return x

    except Exception:
        print("Error while gathering information from database")

def table_columns(table):
    data = ""
    my_curser.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'")

    for i in my_curser:
        data += ' ' + i[3]
    data = data.split(" ")
    data.pop(0)

    return data




if __name__ == "__main__":
    '''in1 = input('Name: ')
    in2 = input('id: ')
    in3 = input('Message: ')'''
    #print(new_table('vid','mention_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50)'))

    add_new(table='vid',name='Non',id=1511515,message='Test_message')
    print('Done... ')
    print(get_table_info('vid',id=False))
    #table_columns('vid')





