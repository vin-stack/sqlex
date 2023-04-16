# Core Pkgs
import streamlit as st 
import base64
import pandas as pd
from streamlit_option_menu import  option_menu
# DB Mgmt
import sqlite3 
from db_fxns import *
conn = sqlite3.connect('data/world.sqlite')
c = conn.cursor()

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("image.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/jpeg;base64,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");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
# Fxn Make Execution
def sql_executor(raw_code):
	c.execute(raw_code)
	data = c.fetchall()
	return data 


city = ['ID,', 'Name,', 'CountryCode,', 'District,', 'Population']
country = ['Code,', 'Name,', 'Continent,', 'Region,', 'SurfaceArea,', 'IndepYear,', 'Population,', 'LifeExpectancy,', 'GNP,', 'GNPOld,', 'LocalName,', 'GovernmentForm,', 'HeadOfState,', 'Capital,', 'Code2']
countrylanguage = ['CountryCode,', 'Language,', 'IsOfficial,', 'Percentage']




def main():
	st.title("SQLSpace")
	
	with st.sidebar:
    		choice = option_menu("SQLSPACE", ["Register","Login"], 
        	icons=['person','key'], menu_icon="server", default_index=1,orientation="horizontal")
    	
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


	elif choice =="Login":
		st.subheader("About")
		username = st.text_input("Username")
		password = st.text_input("Password",type='password')
		if st.checkbox("Login"):
			create_usertable()
			result = login_user(username,password)
			# result = login_user_unsafe(username,password)
			# if password == "12345":
			if result:
				st.success("Logged In as {}".format(username))
				with st.sidebar:
					
    					choice = option_menu( menu_title=None,options=["Cluster","Table", 'Query','Cluster Admin'],
        				icons=['people','table', 'code','track'],default_index=1,orientation="vertical")

				task = st.selectbox("Task",["Add Posts","Analytics","Manage"])

				if task == "Add Posts":
					st.subheader("Add Posts")

				elif task == "Analytics":
					st.subheader("Analytics")

				elif task == "Manage":
					st.subheader("Manage Blog")
					users_result = view_all_users()
					clean_db = pd.DataFrame(users_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorrect Username/Password")

	else:
		st.subheader("Create An Account")
		new_username = st.text_input("User name")
		new_password = st.text_input("Password",type='password')
		confirm_password = st.text_input('Confirm Password',type='password')

		if new_password == confirm_password:
			st.success("Valid Password Confirmed")
		else:
			st.warning("Password not the same")

		if st.button("Sign Up"):
			create_usertable()
			add_userdata(new_username,new_password)
			st.success("Successfully Created an Account")



if __name__ == '__main__':
	main()

