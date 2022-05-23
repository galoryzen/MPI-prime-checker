from mpi4py import MPI
import sys
import time

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

k = int(sys.argv[1])
q = int(sys.argv[2])

times = 0
total = 0
primos_procesados = 0
lista_primos = []

lp = [10**(k-1),10**k]

def primeCheck(num):
    divisores = 0
    for i in range(2, num):
        if num % i == 0:
            divisores += 1
            break

    if divisores == 0:
        return True
    else:
        return False

start = time.time()

if rank == 0:
    for i in range(1, size):

        if (lp[1] - lp[0]) >= 10:
            comm.send([lp[0], (lp[0]+10)], dest=i)
            lp[0] = lp[0] + 10

        elif (lp[1] - lp[0]) == 0:
            continue

        else:
            comm.send([lp[0], lp[1]],dest=i)
            lp[0] = lp[1]
else:
    if q==1:
        data = comm.recv(source = 0)
        cont = 0
        for num in range(data[0], data[1]):
            if primeCheck(num):
                cont+=1
        total += cont
        times = times + 1
        comm.send(rank, dest = 0)

    else:
        data = comm.recv(source = 0)
        for num in range(data[0], data[1]):
            primos_procesados += 1
            if primeCheck(num):
                comm.send([rank, num], dest=0)
                break
        else:
            comm.send([rank, -1], dest=0)

lp = comm.bcast(lp, root=0)
lista_primos = comm.bcast(lista_primos, root=0)


if q==1:
    while lp[1] - lp[0] != 0:
        if rank == 0:
            data = comm.recv()
            if (lp[1] - lp[0]) > 10:                
                comm.send([lp[0], (lp[0]+10)], dest=data)

                lp[0] = lp[0] + 10

            elif (lp[1] - lp[0]) == 0:
                comm.send([-1, -1],dest=data)
            else:
                comm.send([lp[0], lp[1]],dest=data)
                lp[0] = lp[1]

        else:
            data = comm.recv(source = 0)
            if data[0] == -1: break
            cont = 0
            for num in range(data[0], data[1]):
                if primeCheck(num):
                    cont+=1
            total += cont
            times = times + 1
            comm.send(rank, dest = 0)
        lp = comm.bcast(lp, root=0) 
else:
    while len(lista_primos) < size-1:
        if rank == 0:
            data = comm.recv()
            if data[1] == -1:
                if (lp[1] - lp[0]) >= 10:
                    comm.send([lp[0], (lp[0]+10)], dest=data[0])
                    lp[0] = lp[0] + 10
                else:
                    comm.send([lp[0], lp[1]], dest=data[0])
                    lp[0] = lp[1]
            else:
                lista_primos.append(data[1])
                comm.send([-1, -1], dest=data[0])
        else:
            data = comm.recv(source=0)
            if data[0] == -1: break

            for num in range(data[0], data[1]):
                primos_procesados += 1
                if primeCheck(num):
                    comm.send([rank, num], dest=0)
                    break
            else:
                comm.send([rank, -1], dest=0)

if q==1:
    if rank == 0:
        for i in range(1, size):
            data = comm.recv()
            comm.send([-1,-1], dest=data)

if q==1:
    total_primos = comm.reduce(total, op=MPI.SUM, root=0)

if q==1:
    if rank == 0:
        print("Tiempo de ejecucion: ",round(time.time()-start, 5), "seconds")
        print("Numero total de primos: ", total_primos)
    else:
        print("El proceso", rank, "verificó", times, "paquetes")
else:
    if rank == 0:
        print("Tiempo de ejecucion: ",round(time.time()-start, 5), "seconds")
        print("Primos Encontrados: ", lista_primos)
    else:
        print("El proceso", rank, "verifico", primos_procesados, "numeros")