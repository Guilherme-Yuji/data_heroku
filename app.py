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
	hue = data.columns[-1]

	st.markdown('**2.1- Descriptive Statistics**')
	st.text(data.describe())

	st.markdown('**2.2- Outlier detectetion by Boxplot**')
	for a in numerical_attributes:
		st.text(a)
		fig = plt.figure(figsize = (20,10))
		sns.boxplot(data[a])
		st.pyplot(fig)


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
	fig = plt.figure(figsize = (20,10))
	sns.heatmap(data.corr(), cmap = 'Blues', annot = True)
	st.pyplot(fig)

	st.markdown('***2.4.2- Distributions***')
	for a in numerical_attributes:
		st.text(a)
		fig = plt.figure(figsize = (20,10))
		sns.histplot(data = data , x =a , kde = True, hue = hue)
		st.pyplot(fig)

	

	st.markdown('**2.5- Categorical Variables**')


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
	

st.write("""
# Data Science App
In this implementation, you can to the EDA of our dataset to speed-up our analysis! \n
To use this app, First you need to import your dateset in the sidebar on the left and then just wait for the results. \n
NOTES: \n
The target variable it will be considered to be the last column of the dataset.
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
    build_model(df)
else:
	st.write("Please, input a dataset")

