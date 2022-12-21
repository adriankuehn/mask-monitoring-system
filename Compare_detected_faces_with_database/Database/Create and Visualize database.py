import os
import sqlite3


""" Either creates a new database based on the profile pictures in the fodler 'profile_pictures' or shows the current
 content of the databases and stroes all entries in the folder 'Show_Pics' """


connection = sqlite3.connect("Profil_Datenbank.db")
cursor = connection.cursor()

def create_new_database():
    # Creates new Database with profile pictures from folder "profilbilder"
    # DB Fields: ID, Vorname, Nachname, Profilbild, Anzahl Verstöße (Bilder Abstand in Video von mehr als 5min = 1 Verstoß)
    try:
        cursor.execute("""DROP TABLE Profile;""")  # delete old table
    except:
        pass
    sql_command = """
    CREATE TABLE Profile ( 
    Person_ID INTEGER PRIMARY KEY, 
    Vorname VARCHAR(20), 
    Nachname VARCHAR(30), 
    Profilbild BLOB NOT NULL,
    Anzahl_Verstöße INTEGER);"""
    cursor.execute(sql_command)

    for name in os.listdir('profile_pictures'):
        path='profile_pictures/'+name
        print ('Path: ', path)
        with open(path, 'rb') as file:
            blob_data = file.read()

        value_id=''
        value_vorn=''
        value_nachn=''
        z_n=0
        for n in name:
            if n=='_':
                z_n += 1
            if z_n==0:
                value_id += n
            elif z_n==1:
                value_vorn += n
            elif z_n==2:
                value_nachn += n
        value_vorn=value_vorn[1:]
        value_nachn=value_nachn[1:]

        data_tuple = (value_id, value_vorn, value_nachn, blob_data, 0)
        query = """ INSERT INTO Profile (Person_ID, Vorname, Nachname, Profilbild, Anzahl_Verstöße) VALUES (?, ?, ?, ?, ?)"""
        cursor.execute(query, data_tuple)
    print("Database was created successfully based on the pictures in the folder 'profile_pictures' !")


def show_pics_database():
    cursor.execute("""SELECT * from Profile""")
    record = cursor.fetchall()
    print(record[0][0])
    for row in record:
        print("Person_ID:", row[0], " Vorname:", row[1], " Nachname:", row[2], " Anzahl_Verstöße:", row[4])
        try:
            os.mkdir('Show_Pics')
        except:
            pass
        pic_path = 'Show_Pics/'+str(row[0])+'_'+str(row[1])+'_'+str(row[2])+'--'+str(row[4])+'.png'
        with open(pic_path, 'wb') as file:
            file.write(row[3])
    print("You can view all the persons in the database and their profile pictures in the folder 'Show_Pics' now."+
          " Do not forget to delete the content of the folder before rerunning this function")


# create_new_database()  # you should comment out one of the two commands
show_pics_database()

connection.commit()  # save changes
connection.close()



