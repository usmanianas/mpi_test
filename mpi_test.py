import numpy as np
import pylab as plt
from matplotlib import cm
import h5py as hp
from mpi4py import MPI
import time
import random 


#### Grid Parameters ###########################
Lx, Ly, Lz = 1.0, 1.0, 1.0

Nx, Ny, Nz = 16, 16, 16

hx, hy, hz = Lx/(Nx-1), Ly/(Ny-1), Lz/(Nz-1)

x = np.linspace(0, 1, Nx, endpoint=True)        
y = np.linspace(0, 1, Ny, endpoint=True)
z = np.linspace(0, 1, Nz, endpoint=True)    

hx2, hy2, hz2 = hx*hx, hy*hy, hz*hz

idx2, idy2, idz2 = 1.0/hx2, 1.0/hy2, 1.0/hz2
#############################################################


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nprocs = comm.Get_size()

locn = int(Nz/nprocs)
bn = 1 + locn*rank
en = bn + locn 

if rank == nprocs-1:
	en = Nz-1


#bn = int((Nx/nprocs)*rank)
#en = int(bn + (Nx/nprocs))

#locE = []

#if rank == 0:
#	bn = 1

#print(rank, bn, en)
'''
if rank == 0:
	locE = 0.01
if rank == 1:
	locE = 0.23
if rank == 2:
	locE = 0.43
if rank == 3:
	locE = 0.46

#totalE = 0#[]#np.zeros(1)

totalE = comm.reduce(locE, op=MPI.SUM, root=0)

if rank == 0:
	print(totalE)

'''	

print(rank, bn, en)


#T = np.zeros([Nx, Ny, Nz])

#T[:, :, 0:Nz] = 1 - z[0:Nz]


T = np.zeros([Nx, Nz])

#T[:, 0:Nz] = 1 - z[0:Nz]
T[:, bn:en] = 1 - z[bn:en]


#print(rank, T[10, bn:en])

print(rank, T[10, :])	


if rank == 0:
	T[:, en] = comm.sendrecv(T[:, en-1], dest = rank+1, source = rank+1)

if rank > 0 and rank < nprocs-1: 
	T[:, en] = comm.sendrecv(T[:, en-1], dest = rank+1, source = rank+1)
	T[:, bn-1] = comm.sendrecv(T[:, bn], dest = rank-1, source = rank-1)

if rank == nprocs-1:
	T[:, bn-1] = comm.sendrecv(T[:, bn], dest = rank-1, source = rank-1)

print(rank, T[10, :])	

'''
if rank == 1:
	print("Temperature", T[:, en-1])
	T[:, en-1] = comm.recv(source = 0)
	print("Temperature", T[:, en-1])
'''


