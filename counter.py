import RPi.GPIO as GPIO
import datetime 
import json
import pymysql

con = pymysql.connect(host='localhost', database ='Datos', user='root', password='root')
contador_inicial=0

#actualizar el valor de la cuenta al último registrado
try:

    with con.cursor() as cur:
        #consulta SQL q toma una sola fila ordenando por id de forma descendiente
        cur.execute('select * from consumo ORDER BY id DESC LIMIT 1;')

        version = cur.fetchone()

        #print(f'Database version: {version[1]}')

        contador_inicial=version[2]


finally:


    con.close()

#prepara los puertos de entrada/salida 
GPIO.setmode(GPIO.BCM) # The GPIO.BCM option means that you are referring to the pins by the "Broadcom SOC channel" number
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)# configura el puerto 23 como entrada en modo pull up
#contador_inicial=0
counter = contador_inicial
consumo_inicial = float(contador_inicial)/2000.
now = datetime.datetime.now()
timestamp = datetime.datetime.timestamp(now)

def consumo_parcial( pulsos):
    return float (pulsos) / 2000.

#borro la siguiente linea para evitar duplicados en la BD 
#data = {"timestamp":timestamp,"fecha":now.strftime("%m/%d/%Y, %H:%M:%S"),"counter":counter,"consumo_total":str(consumo_inicial + consumo_parcial(counter))}
#print (json.dumps(data))


while True:
    GPIO.wait_for_edge(23, GPIO.RISING)
    GPIO.wait_for_edge(23, GPIO.FALLING)
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    counter += 1
    data = {"timestamp":timestamp,"fecha":now.strftime("%m/%d/%Y, %H:%M:%S"),"counter":counter,"consumo_total":consumo_inicial + consumo_parcial(counter)}
    #print ("Counter is now", counter, "pulsos", "consumo", consumo_inicial + consumo_parcial(counter))
    print (json.dumps(data))
    

GPIO.cleanup()
