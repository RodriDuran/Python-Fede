import pymysql
import csv
import subprocess
import sys
import datetime
#print ("que era")
con = pymysql.connect(host='localhost', database='Datos',
    user='root', password='root')

fecha_inicial = sys.argv[1]
fecha_final = sys.argv[2]
fecha_i=fecha_inicial.split("/")
fecha_f=fecha_final.split("/")
#print (fecha_i)
#print (fecha_f)

fecha_obj_i=datetime.datetime(int (fecha_i[0]),int (fecha_i[1]),int (fecha_i[2]))
fecha_obj_f=datetime.datetime(int (fecha_f[0]),int (fecha_f[1]),int (fecha_f[2]))
timestamp_i= datetime.datetime.timestamp(fecha_obj_i)
timestamp_f= datetime.datetime.timestamp(fecha_obj_f)
#print ("time i: ",timestamp_i)
#print ("time f: ",timestamp_f)
try:

    with con.cursor() as cur:

        cur.execute('select * from ambiente where date >='+str(timestamp_i)+' and date <='+str(timestamp_f)+ ';')
        version = cur.fetchall()
        archivo="consulta-ambiente.csv"
        csvfile=open(archivo,'w', newline='')
        obj=csv.writer(csvfile)
        obj.writerow(['id','date','temperatura','humedad'])
        cantidad_lineas=0

        for row in version:
            obj.writerow(row)
            cantidad_lineas=cantidad_lineas+1
        csvfile.close()
        copy=subprocess.run(["scp", archivo,"perico@45.15.25.196:~"])
        
        #print(f'Database version: {version[1]}')
        print (cantidad_lineas ," Registros")
        


finally:


    con.close()