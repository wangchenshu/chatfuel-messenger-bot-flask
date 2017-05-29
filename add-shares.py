# -*- coding: utf-8 -*- 
import mysql.connector

file_name = 'serial-all.csv'

f = open(file_name,  'r')

i = 0
cnx = mysql.connector.connect(user='root',
                              password='iamwalter',
                              host='127.0.0.1',
                              port=32768,
                              database='home')

cursor = cnx.cursor()
for line in f:
    if i == 0: 
        pass
        i += 1
    else:
        datas = line.split(',')
        serial = datas[0]
        date = datas[1]
        company = datas[2]
        phonetic = datas[3]
        souvenirs = datas[4]
        seeking_people = datas[5]
        print 'serial: ' + serial
        print 'date: ' + date
        print 'company: ' + company
        #print 'phonetic: ' + phonetic
        print 'souvenirs: ' + souvenirs
        print 'seeking_people: ' + seeking_people
        print ''

        data_share = (serial, date, company, phonetic, souvenirs, seeking_people)
        add_share = ("INSERT INTO request "
                        "(serial, date, company, phonetic, souvenirs, seeking_people) "
                        "VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(add_share, data_share)
        cnx.commit()
cursor.close()
cnx.close()