import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Formula import formula_capasitor
import plotly.graph_objects as go
import plotly.figure_factory as ff
from Graph import create_graph_potential_Cap,Electric_Field_Plot

def teks1():
    st.subheader("Persamaan Poison 📚")
    st.text("Pada potensial kapasitor dua plat, potensialnya digambarkan dalam bentuk persamaan berikut")
    st.latex(r'''
    \nabla^2 V = \frac{\rho}{\epsilon_0}         
    ''')
    st.text("Dengan menggunakan Metode Beda Hingga dapat diubah menjadi bentuk persamaan berikut")
    st.latex(r'''
    V_{i,j} = \frac{4V_{i+1,j} + V_{i-1,j} + V_{i,j+1} + V_{i,j-1}-\frac{\rho_{i,j}h^2}{\epsilon}}{4}

    ''')
    st.text("Kemudian terapkan Syarat Neumann untuk semua batas")
    st.latex(r'''
    \frac{\partial V}{\partial y}(y=0)=0  \iff \frac{V_{0,j+1}-V_{0,j}}{h_y}=0 \rightarrow V_{0,j+1}=V_{0,j}\\
    \frac{\partial V}{\partial x}(x=0)=0 \iff \frac{V_{i+1,0}-V_{i,0}}{h_x}=0 \rightarrow V_{i+1,0}=V_{i,0}\\         
    \frac{\partial V}{\partial x}(x=L)=0 \iff \frac{V_{i+1,j}-V_{i,j}}{h_x}=0 \rightarrow V_{i+1,j}=V_{j}\\         
    \frac{\partial V}{\partial x}(y=L)=0 \iff \frac{V_{i,j+1}-V_{i,j}}{h_x}=0 \rightarrow V_{i+1,j}=V_{i,j}\\         
    ''')
    st.text("Dan implementasi kode python diberikan dalam bentuk berikut")
    st.code('''
import numpy as np
import matplotlib.pyplot as plt
from numba import jit

# Parameter grid
Nx, Ny = 50, 50  # Ukuran grid


# Parameter fisik
rho = np.zeros((Nx, Ny))  # Distribusi muatan
epsilon = 8.85e-12  # Permitivas listrik (dalam SI, opsional)

# Menempatkan pelat bermuatan di tengah grid (garis horizontal)
pos_y1 = Ny // 4
pos_y2 = 3*Ny // 4
pos_x1 = Nx //4
pos_x2 = 3*Nx //4
rho[pos_x1, pos_y1:pos_y2] = 1e-9 #plat 1 di posisi x1
rho[pos_x2, pos_y1:pos_y2] = 1e-9 #plat 2 di posisi x2

# Iterasi Gauss-Seidel untuk menyelesaikan persamaan Poisson

@jit
def sol_of_potcap():
  V = np.zeros((Nx, Ny))  # Inisialisasi potensial
  tol = 1e-5
  max_iter = 5000
  h2 = 1  # Asumsi grid spacing 1 unit
  for _ in range(max_iter):
      V_old = V.copy()
      for i in range(1, Nx-1):
          for j in range(1, Ny-1):
              V[i, j] = 0.25 * (V[i+1, j] + V[i-1, j] + V[i, j+1] + V[i, j-1] - rho[i, j] * h2 / epsilon)
      # Terapkan kondisi batas Neumann di semua tepi grid
              V[0, :] = V[1, :]       # Batas kiri
              V[Nx-1, :] = V[Nx-2, :] # Batas kanan
              V[:, 0] = V[:, 1]       # Batas bawah
              V[:, Ny-1] = V[:, Ny-2] # Batas atas
      if np.max(np.abs(V - V_old)) < tol:
          break  # Konvergen
  return V

V = sol_of_potcap()
# Plot hasil
plt.figure(figsize=(8,6))
CS = plt.contour(V.T, levels=50)  # Transpose agar orientasi benar # Store the contour object in CS
plt.clabel(CS, CS.levels, inline=True, fontsize=6) # Use CS to access the levels
plt.colorbar(label='Potensial (V)')
plt.title("Distribusi Potensial dalam Kapasitor 2D")
plt.xlabel("x")
plt.ylabel("y")
plt.vlines(pos_x1, ymin=pos_y1, ymax=pos_y2, color='r')
plt.vlines(pos_x2, ymin=pos_y1, ymax=pos_y2, color='b')
plt.show()
    ''')
def app():
    
    st.title("Potensial pada Kapasitor💡")
    teks1()
    st.subheader("Solusi dan Visualisasi 🔬")
    st.warning("Proses Running begitu lama, Mohon ditunggu")
    Nx = st.slider("jumlah grid", 0, 200, 50)
    max_iter = st.slider("Maksimus Iterasi", 0, 5000, 5000)

    panjang_y = st.slider("Panjang plat", 0, 64,16)
    jarak_plat = st.slider("Jarak kedua plat", 0, 64,16)
    sol,posisi = formula_capasitor(Nx,max_iter,jarak_plat,panjang_y)
    fig = create_graph_potential_Cap(sol,posisi)
    st.pyplot(fig)
    Fig = Electric_Field_Plot(sol,Nx,posisi)

    st.markdown('''
    Lalu untuk mencari medan listriknya gunakan persamaan
    ''')
    st.latex(r'''
    \vec{E} = -\nabla V
    ''')
    st.text("Dalam bentuk komponen")
    st.latex(r'''
    E_x = -\frac{\partial V}{\partial y},E_y = -\frac{\partial V}{\partial x} 
    ''')
    st.latex(r'''
    E_x[i,j] = -\frac{V[i+1,j] - V[i-1,j]}{2h}
    ''')
    st.text("atau")
    st.latex(r'''
     E_x[i,j] = -\frac{V[i+1,j] - V[i-1,j]}{2h}, E_y[i,j] = -\frac{V[i,j+1] - V[i,j-1]}{2h}
    ''')
    st.markdown(
        '''
    Hal diatas dapat dihitung mengggunakan atribut```gradient``` dari Library Numpy.
    '''
    )
    st.code('''
    # Menghitung gradien potensial untuk mendapatkan medan listrik
    Ey, Ex = np.gradient(-V.T)  # Perhatikan tanda negatif untuk medan listrik

    x, y = np.meshgrid(np.arange(Nx),
                       np.arange(Ny))

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

    ''')
    on = st.toggle("Ketuk untuk melihat Kurva medan listrik")
    if on:
        st.plotly_chart(Fig)
