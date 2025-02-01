import streamlit as st
import numpy as np
from Graph import create_plot_FD,create_plot_second_FD
import matplotlib.pyplot as plt

def app():
    # Penjelasan Finite Difference
    st.title("Finite Difference💡")
    #st.subheader("Pengantar Metode Finite Difference 🚀")
    st.markdown(
        '''
        **Finite Difference** adalah metode numerik yang digunakan untuk menghitung turunan fungsi secara diskret.
        Metode ini berguna dalam penyelesaian persamaan diferensial numerik.
        
        Tiga pendekatan utama:
        '''
    )
    st.subheader("Turunan Pertama 🧮")
    st.text("Untuk turunan pertama diberikan dalam bentuk matematis sebagai berikut")
    st.latex(r'''
    \text{Forward Difference}\rightarrow f'(x) = \frac{f(x+h) - f(x)}{h} \\
    \text{Backward Difference} \rightarrow f'(x) = \frac{f(x) - f(x-h)}{h} \\
    \text{Central Difference} \rightarrow f'(x) = \frac{f(x+h) - f(x-h)}{2h} \\

    ''')

    # Pilihan fungsi
    fungsi_pilihan = st.selectbox("Pilih fungsi:", ["sin(x)", "exp(x)", "x^2"])

    # Definisi fungsi
    # Definisi fungsi
    if fungsi_pilihan == "sin(x)":
        f = np.sin
        df = np.cos
    elif fungsi_pilihan == "exp(x)":
        f = np.exp
        df = np.exp
    else:
        f = lambda x: x**2
        df = lambda x: 2*x
    st.text("Semakin besar kecil nilai h, maka hasil turunan dari fungsi tersebut akan mendekati solusi analitiknya")
    # Parameter
    h = st.slider("Pilih nilai h:", 0.01, 1.0, step=0.01)
    x = np.linspace(-2, 2, 100)
    # Plot
    fig,fig2 = create_plot_FD(x,f,df,h,fungsi_pilihan)
    st.pyplot(fig)
    st.pyplot(fig2)

    st.subheader("Turunan kedua 🌍")
    st.markdown(
    """
        Sedangkan **Metode Finite Difference untuk Turunan Kedua** digunakan untuk menghitung turunan kedua dari suatu fungsi secara numerik.

        Formula yang digunakan:
        """
    )
    st.latex(r'''
    \text{Second Central Difference} \rightarrow f''(x)=\frac{f(x+h) - 2f(x) + f(x-h)}{h^2}
        
    ''')

    # Pilihan fungsi
    fungsi_pilihan = st.selectbox("Pilih fungsi:", ["sin(x)", "exp(x)", "x^2", "x^3"])

    # Definisi fungsi dan turunannya
    if fungsi_pilihan == "sin(x)":
        f = np.sin
        d2f = lambda x: -np.sin(x)
    elif fungsi_pilihan == "exp(x)":
        f = np.exp
        d2f = np.exp
    elif fungsi_pilihan == "x^2":
        f = lambda x: x**2
        d2f = lambda x: 2*np.ones_like(x)
    else:
        f = lambda x: x**3
        d2f = lambda x: 6*x

    # Parameter
    h = st.slider("Pilih nilai h:", 0.01, 1.0, 0.1, step=0.01)
    x = np.linspace(-2, 2, 100)
    fig3,fig4 = create_plot_second_FD(x,f,d2f,h,fungsi_pilihan)
    st.pyplot(fig3)
    st.pyplot(fig4)

