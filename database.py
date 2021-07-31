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

def new_database(name):
    # UNSIGNED no - or +
    my_curser.execute(f'CREATE TABLE {name} (mention_ID int PRIMARY KEY AUTO_INCREMENT,name VARCHAR(50),id int(20) UNSIGNED,date VARCHAR(50),message VARCHAR(50))')
    return "Completed"

def add_new(name,id,message): # Insert new details
    try:
        my_curser.execute(f'INSERT INTO id_list (name,id,date,message) VALUES {(name, id, str(date)+" "+str(times), message)}')
        print("committing")
        db.commit()
        print("Data saved successfully in database")
    except Exception:
        print("Error while adding to database")


def get_table_info(table):
    try:
        my_curser.execute(f'SELECT * FROM {table}')
        x = []
        for i in my_curser:
            x.append(i[2])
        print("Data imported successfully")
        return x
    except Exception:
        print("Error while gathering information from database")


if __name__=="__main__":
    '''in1 = input('Name: ')
    in2 = input('id: ')
    in3 = input('Message: ')'''
    #print(new_database('id_list'))

    #add_new(name='Null',id=15115511515,message='Previous messages')
    print('Done... ')
    print(get_table_info('id_list'))






