import streamlit as st
from streamlit_option_menu import option_menu
import Laplace,Capacitor,Pengantar
import streamlit as st
# Set konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Finite Difference",
    page_icon="🌟"  
)

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Finite Difference',
                options=["Kapasitor","Pengantar Finite Difference","Persamaan Poisson"],
                menu_icon='book-fill',
                icons=['calculator','bar-chart','thermometer-half','info-circle-fill'],#,'trophy-fill','info-circle-fill'

                default_index=1,
        #         styles={
        #             "container": {"padding": "5!important","background-color":'black'},
        # "icon": {"color": "white", "font-size": "23px"}, 
        # "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        # "nav-link-selected": {"background-color": "#02ab21"},}      
                )
        if app=="Pengantar Finite Difference":
            Pengantar.app()
        if app=="Kapasitor":
            Capacitor.app()
        if app=="Persamaan Poisson":
            Laplace.app()
    run()            
         