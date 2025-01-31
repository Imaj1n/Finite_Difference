import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
from Formula import FD,FD2
from numba import jit

def create_plot_FD(x,f,df,h,fungsi_pilihan):
    y_forward,y_backward,y_central,x_diff,error_forward,error_backward,error_central = FD(h,f,df)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, f(x), label=f"{fungsi_pilihan}")
    ax.plot(x_diff, y_forward, 'r--', label="Forward Difference")
    ax.plot(x_diff, y_backward, 'g--', label="Backward Difference")
    ax.plot(x_diff, y_central, 'b--', label="Central Difference")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("f(x) atau turunan numerik")

    #error plot
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(x_diff, error_forward, 'r--', label="Error Forward Difference")
    ax2.plot(x_diff, error_backward, 'g--', label="Error Backward Difference")
    ax2.plot(x_diff, error_central, 'b--', label="Error Central Difference")
    ax2.legend()
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    return fig,fig2

def create_plot_second_FD(x,f,d2f,h,fungsi_pilihan):
    x_diff,y_true,y_second_central,error_second_central = FD2(h,f,d2f)
    
    # Plot hasil turunan kedua
    figa, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, f(x), label=f"{fungsi_pilihan}")
    ax.plot(x_diff, y_second_central, 'b--', label="Second Central Difference")
    ax.legend()
    ax.set_xlabel("x")
    ax.set_ylabel("f(x) atau turunan kedua numerik")
    # Plot Error
    figb, ax2 = plt.subplots(figsize=(6, 4))
    ax2.plot(x_diff, error_second_central, 'r--', label="Error Second Central Difference")
    ax2.legend()
    ax2.set_xlabel("x")
    ax2.set_ylabel("Error")
    return figa,figb

def create_graph_poisson(L,nx,ny,phi1):
    X, Y = np.meshgrid(np.linspace(0, L, nx), np.linspace(0, L, ny))
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    ax3.legend()
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    # Membuat plot contour
    cf = ax3.contourf(X, Y, phi1.T, 20, cmap='viridis')
    # Menambahkan colorbar
    cbar = fig3.colorbar(cf, ax=ax3)
    cbar.set_label('$\phi$')  # Label colorbar
    return fig3

def create_graph_potential_Cap(V,position):
    pos_x1,pos_x2,pos_y1,pos_y2=position
    plt.figure(figsize=(8,6))
    CS = plt.contour(V.T, levels=50)  # Transpose agar orientasi benar # Store the contour object in CS
    plt.clabel(CS, CS.levels, inline=True, fontsize=6) # Gunakan CS 
    plt.colorbar(label='Potensial (V)')
    plt.title("Distribusi Potensial dalam Kapasitor 2D")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.vlines(pos_x1, ymin=pos_y1, ymax=pos_y2, color='r')
    plt.vlines(pos_x2, ymin=pos_y1, ymax=pos_y2, color='b')
    return plt

def Electric_Field_Plot(V, Nx, position):
    pos_x1, pos_x2, pos_y1, pos_y2 = position
    
    # Menghitung gradien potensial untuk mendapatkan medan listrik
    Ey, Ex = np.gradient(-V.T)  # Perhatikan tanda negatif untuk medan listrik

    x, y = np.meshgrid(np.arange(Nx),
                       np.arange(Nx))

    # Membuat quiver plot dengan Plotly
    fig = ff.create_quiver(x, y, 
                           u=Ex, v=Ey,
                           scale=0.02,  # Menyesuaikan skala panah
                           arrow_scale=0.5,
                           name='Medan Listrik')

    # Menambahkan garis untuk pelat kapasitor (opsional)
    fig.add_shape(
        type="line",
        x0=pos_x1, y0=pos_y1,
        x1=pos_x1, y1=pos_y2,
        line=dict(color="red", width=2)
    )

    fig.add_shape(
        type="line",
        x0=pos_x2, y0=pos_y1,
        x1=pos_x2, y1=pos_y2,
        line=dict(color="blue", width=2)
    )

    # Mengatur ukuran canvas agar berbentuk persegi
    fig.update_layout(
        width=600,  # Lebar canvas
        height=800,  # Tinggi canvas (sama dengan lebar untuk persegi)
        title="Medan Listrik",  # Judul plot
        xaxis=dict(scaleanchor="y"),  # Menjaga rasio x dan y tetap sama
        yaxis=dict(scaleanchor="x")   # Menjaga rasio x dan y tetap sama
    )

    return fig