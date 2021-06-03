import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Page layout
## Page expands to full width
st.set_page_config(page_title='Data Science App',
    layout='wide')



# Model building
def build_model(data):

	global target_variable


	st.markdown('**1.2- Dataset general info**')
	st.text('Dataset shape:')
	st.text(df.shape)

	categorical_attributes = list(data.select_dtypes(include=['object']).columns)
	st.text("Categorical Variables:")
	st.text(categorical_attributes)

	numerical_attributes = list(data.select_dtypes(include=['float64', 'int64']).columns)
	st.text("Numerical Variables:")
	st.text(numerical_attributes)


	st.markdown('**1.3- Duplicated values**')
	st.text(data.duplicated().sum())

	st.markdown('**1.4- Missing values**')
	st.text(data.isnull().sum())

	st.markdown('**1.5- Unique values in the Categorical Variables**')
	for col_name in data.columns:
		 if data[col_name].dtypes == 'object':
		 	unique_cat = len(data[col_name].unique())
 			st.text("Feature '{col_name}' has {unique_cat} unique categories".format(col_name=col_name, unique_cat=unique_cat))
	

	st.subheader('2- Exploratory Data Analysis (EDA)')
	hue = target_variable

	st.markdown('**2.1- Descriptive Statistics**')
	st.text(data.describe())

	st.markdown('**2.2- Outlier detectetion by Boxplot**')
	if len(numerical_attributes) == 0:
		st.text('There is no numerical variable')
	else:	
		for a in numerical_attributes:
			st.text(a)
			fig = plt.figure(figsize = (20,10))
			sns.boxplot(data[a])
			st.pyplot(fig)


	if data[target_variable].dtypes == 'O':
		catplots(data)
	else:
		if len(data[target_variable].unique()) > 5:
			numplots(data)
		else:
			catplots(data)

	

def catplots(data):

	global target_variable
	hue = target_variable

	categorical_attributes = list(data.select_dtypes(include=['object']).columns)
	numerical_attributes = list(data.select_dtypes(include=['float64', 'int64']).columns)

	st.markdown('**2.3- Target Variable plot**')
	st.text("Target variable:" + hue)
	fig = plt.figure(figsize = (20,10))
	ax = sns.countplot(data[hue])
	for p in ax.patches:
		height = p.get_height()
		ax.text(x = p.get_x()+(p.get_width()/2), y  = height*1.01, s = '{:.0f}'.format(height), ha = 'center')
	st.pyplot(fig)


	st.markdown('**2.4- Numerical Variables**')
	#fig = plt.figure(figsize = (5,5))
	#sns.pairplot(data, hue = hue)
	#st.pyplot(fig)

	st.markdown('***2.4.1- Correlation***')

	try:
		fig = plt.figure(figsize = (20,10))
		sns.heatmap(data.corr(), cmap = 'Blues', annot = True)
		st.pyplot(fig)
	except:
		st.text('There is no numerical variable')


	st.markdown('***2.4.2- Distributions***')
	for a in numerical_attributes:
		st.text(a)
		fig = plt.figure(figsize = (20,10))
		sns.histplot(data = data , x =a , kde = True, hue = hue)
		st.pyplot(fig)

	

	st.markdown('**2.5- Categorical Variables**')

	if len(categorical_attributes) == 0:
		st.text('There is no categorical variable')

	else:
		for a in categorical_attributes:
			if a == hue:
				pass
			else:
				st.text(a)
				fig = plt.figure(figsize = (20,10))
				ax = sns.countplot(y = data[a], hue = data[hue])
				for p in ax.patches:
					width = p.get_width()
					ax.text(x = width*1.01, y  = p.get_y()+(p.get_height()/2), s = '{:.0f}'.format(width), va = 'center')
				plt.legend(loc='upper left')
				st.pyplot(fig)


def numplots(data):
	st.text('Under construction')
	global target_variable
	hue = target_variable

	categorical_attributes = list(data.select_dtypes(include=['object']).columns)
	numerical_attributes = list(data.select_dtypes(include=['float64', 'int64']).columns)

	st.markdown('**2.3- Target Variable plot**')
	st.text("Target variable:" + hue)
	fig = plt.figure(figsize = (20,10))
	sns.histplot(data = data , x = hue , kde = True)
	st.pyplot(fig)

	
	st.markdown('**2.4- Numerical Variables**')
	if len(numerical_attributes) == 0:
		st.text('There is no categorical variable')

	else:
		for a in numerical_attributes:
			if a == hue:
				pass

			else:
				st.text(a)
				fig = plt.figure(figsize = (20,10))
				fig = sns.lmplot(data = data, x = a, y = hue)
				st.pyplot(fig)



	st.markdown('**2.5- Categorical Variables**')

	if len(categorical_attributes) == 0:
		st.text('There is no categorical variable')

	else:
		for a in categorical_attributes:
			if a == hue:
				pass
			else:
				st.text(a)
				fig = plt.figure(figsize = (20,10))
				sns.kdeplot(data = data, x = hue ,hue = a)
				st.pyplot(fig)



st.write("""
# Data Science App
In this implementation, you can do the EDA of our dataset to speed-up your analysis! \n
To use this app, follow the steps: \n 
1º - Import your dateset in the sidebar on the left. \n
2º - Choose the target variable on sidebar. \n
3º - Click on the confirmation button to run the app and just wait for the results.
""")


# In[ ]:


# Sidebar - Collects user input features into dataframe
with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/dataprofessor/data/master/delaney_solubility_with_descriptors.csv)
""")


# Main panel

# Displays the dataset
st.subheader('1- Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**1.1. Dataset info:**')
    st.write('First 5 rows of the dataset:')
    st.write(df.head())
    st.write('Last 5 rows of the dataset:')
    st.write(df.tail())
    checker = False


    with st.sidebar.header('2. Select the target variable'):
    	target_variable = st.sidebar.selectbox('Select the target variable', list(df.columns))

    	if st.sidebar.button("Click to confirm the target variable"):
	    	checker = True

    if checker == True:
    	build_model(df)

else:
	st.write("Please, input a dataset")

