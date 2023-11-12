from streamlit_option_menu import option_menu 

def get_selected_option():
    return option_menu(menu_title=None, 
                       options=["Account", "Set Budget", "Tracker", "Report"], 
                       icons=["coin", "database-fill", "bar-chart"], 
                       orientation="horizontal")