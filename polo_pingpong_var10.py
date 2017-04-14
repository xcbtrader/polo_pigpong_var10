__author__ = 'xcbtrader'
# -*- coding: utf-8 -*-

import poloniex
import time
import sys

def guardar_ordenes(cabecera, t1, t2, t3):
	fecha = str(time.strftime("%d/%m/%y")) + ' ' + str(time.strftime("%H:%M:%S"))
	fOrdenes = open('polo_pingpong_var10_ordenes.txt', 'a')
	fOrdenes.write(cabecera + ';' + fecha + ';' + t1 + ';' + t2 + ';' + t3 + '\n')
	fOrdenes.close()

def leer_operativa():
	fOperativa = open('polo_pingpong_var10_operativa.txt', 'a')
	fOperativa.close()
	fOperativa = open('polo_pingpong_var10_operativa.txt', 'r')
	op = fOperativa.readline()
	op = int(op)
	fOperativa.close()
	return op

def leer_ordenes():
	global polo
	try:
		openOrders = polo.returnOpenOrders('USDT_BTC')
		return openOrders
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
		print('### ERROR AL LEER LAS ORDENES ABIERTAS ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)

def realizar_compra(last,margen, saldoUSDTinv):
	global polo, ultimo_precio_buy, ultimo_precio_sell

	precio_compra = last - (last * margen)
	
	try:
		make_order_buy = polo.buy('USDT_BTC',precio_compra,saldoUSDTinv/precio_compra)
		guardar_ordenes('CREADA ORDEN COMPRA', make_order_buy['orderNumber'], str(precio_compra), str(saldoUSDTinv))
		print('-------------------------------------------------------')
		print('*** CREADA ORDEN DE COMPRA NUM ' + make_order_buy['orderNumber'] + ' - PRECIO: ' + str(precio_compra) + ' $ - IVERSION: ' + str(saldoUSDTinv) + ' - BTC: ' + str(saldoUSDTinv/precio_compra) + ' ***')
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
		print('### ERROR AL CREAR ORDEN DE COMPRA ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)	
	
def realizar_venta(last, margen, saldoBTCinv):
	global polo, ultimo_precio_buy, ultimo_precio_sell
	
	precio_venta = last + (last * margen)
	
	try:
		make_order_sell = polo.sell('USDT_BTC', precio_venta, saldoBTCinv)
		guardar_ordenes('CREADA ORDEN VENTA', make_order_sell['orderNumber'], str(precio_venta), str(saldoBTCinv))
		print('*** CREADA ORDEN DE VENTA NUM ' + make_order_sell['orderNumber'] + ' - PRECIO: ' + str(precio_venta) + ' $ - IVERSION: ' + str(saldoBTCinv) + ' - USD: ' + str(saldoBTCinv * precio_venta) + ' ***')
		print('-------------------------------------------------------')	
	except KeyboardInterrupt:
		exit()	
	except Exception:
		print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
		print('### ERROR AL CREAR ORDEN DE VENTA ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)
			
def realizar_ordenes(margen, saldoUSDT, saldoUSDTinv, saldoBTC, saldoBTCinv):
	global polo, n_buy, n_sell

	last = leer_ticker()
		
	if last > 100:
		if n_buy <= 10:
			realizar_compra(last,margen, saldoUSDTinv)
			time.sleep(15)
		else:
			print('### ERROR - SE HAN ABIERTO YA 10 COMPRAS CONSECUTIVAS - ESPERANDO REBOTE ###')
			time.sleep(120)
			
		if n_sell <= 10:
			realizar_venta(last, margen, saldoBTCinv)
		else:
			print('### ERROR - SE HAN ABIERTO YA 10 VENTAS CONSECUTIVAS - ESPERANDO REBOTE ###')
			time.sleep(120)
					
		print('### ORDENES REALIZADAS CORRECTAMENTE - ESPERANDO 2 MINUTOS ###')
		time.sleep(120)
	else:
		print('### ERROR AL LEER VALOR ACTUAL btc ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)		

def leer_balance():
	global polo

	err = True
	while err:
		try:
			balance = polo.returnBalances()
			saldoUSDT = float(balance['USDT'])
			saldoBTC = float(balance['BTC'])
			return saldoUSDT, saldoBTC
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL LEER SALDOS DE LA CUENTA ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)	
		
def crear_ordenes(margen, saldoUSDTinv, saldoBTCinv):

		
	if saldoBTC < 0.0005 or saldoUSDT < 1:
		print('### ERROR SALDO INSUFICIENTE PARA REALIZAR ORDEN ###')
		print('### ESPERANDO NUEVO SALDO ###')
		time.sleep(120)
	else:
		realizar_ordenes(margen, saldoUSDT, saldoUSDTinv, saldoBTC, saldoBTCinv)	

def leer_ticker():
	global polo

	err = True
	while err:
		try:		
			ticker = polo.returnTicker()
			t = ticker['USDT_BTC']
			last = float(t['last'])
			return last
		except KeyboardInterrupt:
			exit()	
		except Exception:
			print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
			print('### ERROR AL LEER PRECIO BTC_USDT ###')
			print('### ESPERANDO 30 SEGUNDOS ###')
			time.sleep(30)		
		
# PROGRAMA PRINCIPAL ##################################################################
global polo, n_buy, n_sell, ultimo_precio_buy, ultimo_precio_sell

print('')
print('**************************************************************')
print('       INICIANDO BOT POLONIEX PingPong VARIABLE 10')
print('**************************************************************')
print('')

API_key = 'NUESTRA API KEY DE POLONIEX'
Secret = 'NUESTRO SECRET DE POLONIEX'

err = True
while err:
	try:
		polo = poloniex.Poloniex(API_key,Secret)
		err = False
		print('### CONECTADO CORRECTAMENTE A LA API DE POLONIEX ###')
		print('')
	except KeyboardInterrupt:
		exit()
	except Exception:
		print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
		print('### ERROR AL CONECTAR CON API POLONEX ###')
		print('### ESPERANDO 30 SEGUNDOS ###')
		time.sleep(30)
		

tot_buy = 0
n_buy = 0
tot_sell= 0
n_sell = 0
inicial = True
ultimo_precio_buy = 0.0
ultimo_precio_sell = 0.0

margen = 0.0
while margen <0.5:
	m = str(input('Entra margen de beneficio (>=0.5) :? '))
	margen = float(m.replace(',','.'))

margen = margen/100
n = 1

while True:
	
	openOrders = leer_ordenes()
	nOrdenes = len(openOrders)
	
	operativa = leer_operativa()
	
	if operativa == 1 or operativa == 2:
		if nOrdenes == 0 : #Escenario sin inversion. Poner 2 ordenes
			if inicial:
				inicial = False
				saldoUSDT, saldoBTC = leer_balance()
				saldoUSDTinv = saldoUSDT/10
				saldoBTCinv = saldoBTC/10
				n_buy += 1
				n_sell += 1
				
			crear_ordenes(margen, saldoUSDTinv, saldoBTCinv)
			
		elif nOrdenes == 1: 	#Escenario Con una orden cerrada y una orden abierta. Hay que cerrarla si hay suficiente saldo para nueva inversion
			
			for no in openOrders:
				num_orden_cerrar = no['orderNumber']
				tipo_orden_cerrar = no['type']
			try:
				if tipo_orden_cerrar == 'sell':
					tot_buy +=1
				elif tipo_orden_cerrar == 'buy':
					tot_sell +=1
				
				saldoUSDT, saldoBTC = leer_balance()
			
				if saldoBTC < 0.0005 or saldoUSDT < 1:
					print('### ERROR SALDO INSUFICIENTE PARA CANCELAR ORDEN ###')
					print('### ESPERANDO QUE SE CIERRE ORDEN PENDIENTE ###')
					time.sleep(120)
				else:
					if tipo_orden_cerrar == 'sell':
						n_buy += 1
						if n_sell > 0:
							n_sell -= 1
					else:
						n_sell += 1
						if n_buy > 0:
							n_buy -= 1
						
					cancelar_orden = polo.cancelOrder(num_orden_cerrar)
					guardar_ordenes('CANCELADA ORDEN', str(num_orden_cerrar), tipo_orden_cerrar, '')
					print('### CANCELADA ORDEN: ' + str(num_orden_cerrar))
					print('### ESPERANDO 2 MINUTOS PARA CONTINUAR ###')
					time.sleep(120)
			except KeyboardInterrupt:
				exit()	
			except Exception:
				print("### ERROR INESPERADO TIPO:", sys.exc_info()[1])
				print('### ERROR AL CANCELAR ORDEN ###')
				print('### ESPERANDO 30 SEGUNDOS ###')
				time.sleep(30)
				
		elif nOrdenes == 2: # Escenario con toda la inversion aun abierta. No hacer nada
			last = leer_ticker()
			
			print('-------------------------------------------------------')
			print(str(n) + ') (' + str(n_buy) + ')Buy Ord: ' + str(tot_buy) + ' - (' + str(n_sell) + ')Sell Ord: ' + str(tot_sell) + ' - btc = ' + str(last) + ' $')
			n +=1
			for orde in openOrders:
				print(orde['type'] + ' - ' + orde['date'] + ' - ' + orde['rate'] + ' $ - ' + orde['amount'] + ' btc')
			print('-------------------------------------------------------')
			print('### ESPERANDO 2 MINUTOS PARA CONTINUAR ###')
			time.sleep(120)
		elif nOrdenes > 2: # Escenario ERROR demasiadas ordenes abiertas
			print('### ERROR - DEMASIADAS ORDENES ABIERTAS - Max 2 ORDENES. Act. ' + str(nOrdenes) + ' ABIERTAS ###')
			print('### ESPERANDO A QUE SE CIERREN ###')
			time.sleep(300)		


	else:
		print ('### PROCESO CANCELADO ###')
		exit()
	if operativa == 2:
		print ('### PROCESO FINALIZADO ###')
		exit()
