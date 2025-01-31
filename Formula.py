import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
from numba import jit

def FD(h,f,df):
    # Finite Difference
    x_diff = np.linspace(-1.5, 1.5, 50)
    y_forward = (f(x_diff + h) - f(x_diff)) / h
    y_backward = (f(x_diff) - f(x_diff - h)) / h
    y_central = (f(x_diff + h) - f(x_diff - h)) / (2*h)

    y_true = df(x_diff)
    # Error
    error_forward = np.abs(y_forward - y_true)
    error_backward = np.abs(y_backward - y_true)
    error_central = np.abs(y_central - y_true)

    return y_forward,y_backward,y_central,x_diff,error_forward,error_backward,error_central

def FD2(h,f,d2f):

    # Finite Difference untuk turunan kedua
    x_diff = np.linspace(-1.5, 1.5, 50)
    y_true = d2f(x_diff)
    y_second_central = (f(x_diff + h) - 2*f(x_diff) + f(x_diff - h)) / h**2

    # Error
    error_second_central = np.abs(y_second_central - y_true)

    return x_diff,y_true,y_second_central,error_second_central

@jit
def poisson(L,nx,ny,max_iterasi):
    deltax = L/nx
    deltay = L/ny

    phi1 = np.zeros((nx,ny))
    for k in range(max_iterasi):
        for j in range(1,nx-1):
            for i in range(1,ny-1):
                phi1[i,j]=(1/(2*(deltax**2+deltay**2)))*(deltay**2*(phi1[i+1,j]+phi1[i-1,j])+deltax**2*(phi1[i,j+1]+phi1[i,j-1])-(deltax**2)*(deltay**2))
        # Syarat batas Neumann (turunan nol di tepi domain) dan dirichlet
        phi1[0, :] = 0  # di x=0
        phi1[-2,:] = phi1[-1,:]  # di x=L
        phi1[:,2] = phi1[:, 1]  # di y=0
        phi1[:, -1] = 0  # di y=L
    # Visualisasi hasil
    return phi1

@jit
def formula_capasitor(Nx,max_iter,distance_cap,len_cap):
    # Parameter grid
    # Nx, Ny = 20, 20  # Ukuran grid
    V = np.zeros((Nx, Nx))  # Inisialisasi potensial
    # Parameter fisik
    rho = np.zeros((Nx, Nx))  # Distribusi muatan
    epsilon = 8.85e-12  # Permitivas listrik (dalam SI, opsional)
    # Menempatkan pelat bermuatan di tengah grid (garis horizontal)
    pos_y1 = len_cap*Nx // 64
    pos_y2 = (64-len_cap)*Nx // 64
    pos_x1 = distance_cap*Nx //64
    pos_x2 = (64-distance_cap)*Nx //64

    rho[pos_x1, pos_y1:pos_y2] = 1e-9  # Muatan pada seluruh garis horizontal
    rho[pos_x2, pos_y1:pos_y2] = 1e-9  # Muatan pada seluruh garis horizontal

    # Iterasi Gauss-Seidel untuk menyelesaikan persamaan Poisson
    tol = 1e-5
    h2 = 1  # Asumsi grid spacing 1 unit
    for _ in range(max_iter):
        V_old = V.copy()
        for i in range(1, Nx-1):
            for j in range(1, Nx-1):
                V[i, j] = 0.25 * (V[i+1, j] + V[i-1, j] + V[i, j+1] + V[i, j-1] - rho[i, j] * h2 / epsilon)
        # Terapkan kondisi batas Neumann di semua tepi grid
                V[0, :] = V[1, :]       # Batas kiri
                V[Nx-1, :] = V[Nx-2, :] # Batas kanan
                V[:, 0] = V[:, 1]       # Batas bawah
                V[:, Nx-1] = V[:, Nx-2] # Batas atas
        if np.max(np.abs(V - V_old)) < tol:
            break  # Konvergen
    return V,[pos_x1,pos_x2,pos_y1,pos_y2]
