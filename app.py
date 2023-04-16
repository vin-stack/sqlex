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
background-image: url("https://media.istockphoto.com/id/1385979011/vector/connection-circuit-networking-modern-logistics-abstract-background-lines.jpg?b=1&s=612x612&w=0&k=20&c=_4OTe-fXmOWRuPX_mJL1wBUMpzi9lknP7qY20jUQg4Y=");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://d2gg9evh47fn9z.cloudfront.net/1600px_COLOURBOX11140963.jpg");
background-position: left; 
background-repeat: no-repeat;
background-attachment: local;
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

