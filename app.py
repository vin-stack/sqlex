# Core Pkgs
import streamlit as st 
import pandas as pd
from streamlit_option_menu import  option_menu
# DB Mgmt
import sqlite3 
conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()


# Fxn Make Execution
def sql_executor(raw_code):
	c.execute(raw_code)
	data = c.fetchall()
	return data 


city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']




def main():
	st.title("SQLPlayground")
	chewoice=option_menu(
    	    menu_title=None,
     	    options=["Home","About"],
    	    icons=["📎","📎","📎","📎"],
    	    orientation="vertical",key="BSDFDS"
	)
	with st.sidebar:
    		choice = option_menu("Main Menu", ["Home", 'Settings'], 
        	icons=['house', 'gear'], menu_icon="cast", default_index=1,orientation="vertical")
    	
	#menu = ["Home","About"]
	#choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("HomePage")

		# Columns/Layout
		col1,col2 = st.beta_columns(2)

		with col1:
			with st.form(key='query_form'):
				raw_code = st.text_area("SQL Code Here")
				submit_code = st.form_submit_button("Execute")

			# Table of Info

			with st.beta_expander("Table Info"):
				table_info = {'city':city,'country':country,'countrylanguage':countrylanguage}
				st.json(table_info)
			
		# Results Layouts
		with col2:
			if submit_code:
				st.info("Query Submitted")
				st.code(raw_code)

				# Results 
				query_results = sql_executor(raw_code)
				with st.beta_expander("Results"):
					st.write(query_results)

				with st.beta_expander("Pretty Table"):
					query_df = pd.DataFrame(query_results)
					st.dataframe(query_df)


	else:
		st.subheader("About")





if __name__ == '__main__':
	main()

