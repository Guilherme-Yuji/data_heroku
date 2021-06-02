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


	st.markdown('**1.3- Basic Statistics**')
	st.text(data.describe())

	st.markdown('**1.4- Missing values**')
	st.text(data.isnull().sum())
	

	st.subheader('2- Exploratory Data Analysis (EDA)')
	hue = data.columns[-1]

	st.markdown('**2.1- Numerical Variables**')
	#fig = plt.figure(figsize = (5,5))
	#sns.pairplot(data, hue = hue)
	#st.pyplot(fig)

	st.text('Correlation:')
	fig = plt.figure(figsize = (20,10))
	sns.heatmap(data.corr(), cmap = 'Blues', annot = True)
	st.pyplot(fig)

	st.text('Distribution:')
	for a in numerical_attributes:
		st.text(a)
		fig = plt.figure(figsize = (20,10))
		sns.histplot(data = data , x =a , kde = True, hue = hue)
		st.pyplot(fig)

	

	st.markdown('**2.2- Categorical Variables**')
	st.text(hue)
	fig = plt.figure(figsize = (20,10))
	ax = sns.countplot(data[hue])
	for p in ax.patches:
			height = p.get_height()
			ax.text(x = p.get_x()+(p.get_width()/2), y  = height*1.01, s = '{:.0f}'.format(height), ha = 'center')
	st.pyplot(fig)

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
In this implementation, you can the do a full analysis of your dataset anf got a DS solution!
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
    st.markdown('**1.1. Dataset:**')
    st.write(df.head())
    st.write(df.tail())
    build_model(df)
else:
	st.write("Please, input a dataset")

