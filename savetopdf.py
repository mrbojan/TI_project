# -*- coding: utf-8 -*-
import pymysql.cursors
from reportlab.pdfgen import canvas
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='zawody',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
myCursor = connection.cursor()

myCursor.execute("""select idZawodnik, Imie, Nazwisko, TOP, BONUS, (TOP+BONUS*0.001) as suma
            from kategoria inner join zawodnik
            on kategoria.idKategoria = zawodnik.Kategoria_idKategoria
            where Nazwa = 'Kobiety'
            order by suma DESC """)



#pierwsze kryterium
result = myCursor.fetchall()

k=6
for i in range(6,k):
    k = k + 1
    if result[6]['TOP']+(result[6]['BONUS']*0.001)==result[k]['TOP']+(result[k]['BONUS']*0.001):
        k=k

myCursor.execute("""DELETE FROM final""")
for i in range(k):
    myCursor.execute("""INSERT INTO final(idFinal,TOP,BONUS,Zawodnik_idZawodnik,proba_top,proba_bonus)
    VALUES (%s,%s,%s,%s,%s,%s);""",(i+1,result[i]['TOP'],result[i]['BONUS'],result[i]['idZawodnik'],10,10))
k=0
c = canvas.Canvas('ex.pdf')
m=0
print((result))
for j in range(6):
    m=m+1
    result[j]['TOP']=str(result[j]['TOP'])
    result[j]['BONUS']=str(result[j]['BONUS'])
    if result[j]['idZawodnik']<10:
        c.drawString(50, 800 - k,str(m) + '.' + 'Id zawodnika: ' + str(result[j]['idZawodnik']) + '   ' + 'TOPÓW: ' + result[j]['TOP'] + ' ' + 'BONUSÓW: ' + 'ł'+result[j]['BONUS'])
    else:
        c.drawString(50,800-k, str(m) + '.' + 'Id zawodnika: ' + str(result[j]['idZawodnik'])+ ' ' + 'TOPÓW: ' + result[j]['TOP'] + ' ' + 'BONUSÓW: ' + result[j]['BONUS'] )
    k = k + 15


c.showPage()
c.save()

connection.commit()
connection.close()