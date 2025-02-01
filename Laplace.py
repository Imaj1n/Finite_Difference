import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from Formula import poisson,FD
from Graph import create_plot_FD,create_graph_poisson
import Gambar 

def teks1():
    st.title("Persamaan Poison 💡")
    st.text("Anggap sebuah Persamaan Poison memiliki bentuk")
    st.latex(r'''
    \nabla^2 \phi = 1         
    ''')
    st.latex(r'''
    \frac{\phi_{i+1,j}+\phi_{i-1,j}-2\phi_{i,j}}{h^2_x}+\frac{\phi_{i,j+1}+\phi_{i,j-1}-2\phi_{i,j}}{h^2_y}=1
    ''')
    st.text("dan persamaan diatas dapat disederhanakan menjadi persamaan")
    st.latex(r'''
    \phi_{i,j} =\frac{1}{2(h_x^2+h_y^2)}[ h_y^2(\phi_{i+1,j}+\phi_{i-1,j})+h_x^2(\phi_{i,j+1}+\phi_{i,j-1})-h_x^2 h_y^2]
    ''')
    col1, col2 = st.columns(2)
    with col1:
        st.image(Gambar.gambar1)
    with col2:
        st.markdown('''Ide dari persamaan diatas adalah untuk mencari nilai $\phi_{i,j}$ yakni dengan cara menggunakan nilai node node tetangganya 
                    $(\phi_{i+1,j},\phi_{i-1,j}\phi_{i,j+1},\phi_{i,j-1})$ seperti pada gambar. 
                    Oleh karena itu untuk kondisi awal gunakan *boundary problem* dimana syarat ini menggunakan 
                    syarat dirichlet dan syarat neuman yang ditunjukkan oleh persamaan berikut''')
    st.markdown('''
        Memberikan :blue-background[Syarat Dirichlet] 
        yaitu memberikan solusi pada fungsi tertentu secara eksplisit.        
        untuk batas ini anggap kondisi dirichlet memberikan nilai fungsi sama dengan nol
        ''')
    st.latex(r'''
    \phi(y=L)=0 \\
    \phi(x=0)=0 \\
    ''')
    st.subheader("Boundary Condition")
    st.text("Syarat syarat ini memberikan suatu tetapan pada titik grid tertentu dan memberikan solusi yg tetap pada domain tertentu. Syarat ini dibagi menjadi dua yaitu:")
    st.markdown('''
    Untuk  :blue-background[Syarat Neumann] 
    yaitu nilai turunan pertama (gradien) dari fungsi pada batas domain atau 
    menetapkan nilai dari turunan fungsi pada grid tertentu. Untuk kasus persaamaan diatas
    ambil turunan pada pinggir grid sama dengan nol

    ''')
    st.latex(r'''
    \frac{\partial \phi}{\partial y}(y=0)=0  \iff \frac{\phi_{j+1}-\phi_{j}}{h_y}=0 \rightarrow \phi_{j+1}=\phi_j\\
    \frac{\partial \phi}{\partial x}(x=L)=0 \iff \frac{\phi_{i+1}-\phi_{i}}{h_x}=0 \rightarrow \phi_{i+1}=\phi         
    ''')
    st.markdown('''
        Namun pada persamaan diatas akan banyak memerlukan iterasi dan 
        akan memakan banyak waktu. Oleh karena itu, hal ini bisa diatas dengan dekorator ```@jit``` dari Pustaka [Numba](https://numba.pydata.org/).Pustaka ini
        Numba menggunakan LLVM *(Low Level Virtual Machine*) untuk mengkompilasi kode python menjadi kode mesin yang lebih Optimal optimal. Untuk kode pythonnya diberikan sebagai berikut''')
    st.code('''
        L = 50
        nx = 150
        ny = 150
        deltax = L/nx
        deltay = L/ny
        max_iterasi = 500

        @jit #tambahkan diatas fungsi dekorator jit
        def poisson():
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
        return phi1
        phi1 = poisson()
        # Visualisasi hasil
        X, Y = np.meshgrid(np.linspace(0, L, nx), np.linspace(0, L, ny))
        plt.contourf(X, Y, phi1.T, 20, cmap='viridis')
        plt.colorbar(label='$\phi$')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Solusi Persamaan Poisson')
        plt.show()                
    ''')

def app():
    teks1()
    st.subheader("Solusi dan Visualisasi 🔬")
    nx = st.slider("jumlah grid pada arah x", 0, 200, 150)
    ny = st.slider("jumlah grid pada arah y", 0, 200, 150)
    L = st.slider("Panjang-Lebar Sumbu", 0, 100, 50)
    max_iter = st.slider("Maksimus Iterasi", 0, 500, 500)
    sol = poisson(L,nx,ny,max_iter)
    plot_sol = create_graph_poisson(L,nx,ny,sol)
    st.pyplot(plot_sol)
   
