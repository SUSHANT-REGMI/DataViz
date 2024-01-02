# Importing the libraries
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Setting page configurations
st.set_page_config(layout='wide', page_icon='📙')

# Function to load Lottie animation
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

file_url = 'https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json'
lottie_book = load_lottieurl(file_url)
st_lottie(lottie_book, speed=1, height=100, key='initial')

# Markdown headers
st.markdown("<h1 style='text-align: center;'> Analysing Book Rating Dataset </h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'> A Web App by <b><a href='https://github.com/SUSHANT-REGMI'> Sushant & Abhinav </a></b></h3>", unsafe_allow_html=True)

# Welcome message and description
st.write('''
Welcome to the Book Analysis App. This app analyses a dataset called "bookrec"
The dataset merges information of the three initial datasets provided:
* **Books**, which contains data about books, such as ISBN, title, author, year of publication, publisher, and image links;
* **Users**, which has data about the users, such as ID, location, and age;
* **Book-Ratings**, which contains information on user ID, ISBN, and rating.

The analysis of this raw data will guide further steps in data preparation and modeling.

*Please, scroll down and navigate through the tabs below to visualize the graphs.*
''')

# Reading the dataset
bookrec = pd.read_csv('bookrec.csv', encoding='latin1')

# Creating a custom template for plotly
custom_template = {'layout':
                   go.Layout(
                       font={'family': 'Helvetica',
                             'size': 14,
                             'color': '#1f1f1f'},

                       title={'font': {'family': 'Helvetica',
                                       'size': 20,
                                       'color': '#f9f9f9'}},

                       legend={'font': {'family': 'Helvetica',
                                        'size': 14,
                                        'color': '#1f1f1f'}},

                       plot_bgcolor='#f2000f',
                       paper_bgcolor='#f22fff'
                   )}

# Creating a slider for filtering by year of publication
selected_year = st.slider("Select Year of Publication:", min_value=1950, max_value=2020, value=(1950, 2020))

# Filter the dataset based on the selected year range
filtered_bookrec = bookrec[(bookrec['year_pub'] >= selected_year[0]) & (bookrec['year_pub'] <= selected_year[1])]

# Plotting the distribution of 'age' using the filtered dataset
fig_age_filtered = px.histogram(filtered_bookrec, x='age', title="<b>Users' Age Distribution</b>", color_discrete_sequence=['#FF7F50'])
fig_age_filtered.update_layout(height=600, width=1000, template=custom_template, xaxis_title='<b>Age</b>',
                               yaxis_title='<b>Count</b>')

# Plotting the top 10 locations with more ratings published using the filtered dataset
fig_lmr_filtered = px.bar(filtered_bookrec.value_counts('location', ascending=False).head(10),
                          x=filtered_bookrec.value_counts('location', ascending=False).head(10),
                          y=filtered_bookrec.value_counts('location', ascending=False).head(10).index,
                          title="<b>Top 10 Locations with More Ratings Published</b>",
                          color_discrete_sequence=['#FF7F50'])
fig_lmr_filtered.update_layout(height=600, width=1000, template=custom_template, xaxis_title='<b>Rating Count</b>',
                               yaxis_title='<b>Location</b>')
fig_lmr_filtered.update_yaxes(automargin=True, title_standoff=10)

# Plotting the top 10 most rated books (by the number of ratings) using the filtered dataset
fig_mrb_filtered = px.bar(filtered_bookrec.value_counts('book_title', ascending=False).head(10),
                          x=filtered_bookrec.value_counts('book_title', ascending=False).head(10),
                          y=filtered_bookrec.value_counts('book_title', ascending=False).head(10).index,
                          title="<b>Top 10 Most Rated Books</b>",
                          color_discrete_sequence=['#FF7F50'])
fig_mrb_filtered.update_layout(height=600, width=1000, template=custom_template, xaxis_title='<b>Rating count</b>',
                               yaxis_title='<b>Books</b>')
fig_mrb_filtered.update_yaxes(automargin=True, title_standoff=10)

# Plotting the top 10 most rated authors (by the number of ratings) using the filtered dataset
fig_mra_filtered = px.bar(filtered_bookrec.value_counts('book_author', ascending=False).head(10),
                          x=filtered_bookrec.value_counts('book_author', ascending=False).head(10),
                          y=filtered_bookrec.value_counts('book_author', ascending=False).head(10).index,
                          title="<b>Top 10 Most Rated Authors</b>",
                          color_discrete_sequence=['#FF7F50'])
fig_mra_filtered.update_layout(height=600, width=1000, template=custom_template, xaxis_title='<b>Rating Count</b>',
                               yaxis_title='<b>Authors</b>')
fig_mra_filtered.update_yaxes(automargin=True, title_standoff=10)

# Plotting the distribution of 'book_rating' using the filtered dataset
fig_br_filtered = px.histogram(filtered_bookrec, x='book_rating', title="<b>Rating Distribution</b>",
                                color_discrete_sequence=['#FF7F50'])
fig_br_filtered.update_layout(height=600, width=1000, template=custom_template, xaxis_title='<b>Rating</b>',
                               yaxis_title='<b>Count</b>', xaxis=dict(tickmode='linear'), bargap=0.1)

# Scatter plot: User Age vs. Book Rating using the filtered dataset
fig_scatter_filtered = px.scatter(filtered_bookrec, x='age', y='book_rating', title="<b>User Age vs. Book Rating</b>",
                                  color_discrete_sequence=['#FF7F50'])
fig_scatter_filtered.update_layout(height=600, width=1000, template=custom_template,
                                    xaxis_title='<b>Age</b>', yaxis_title='<b>Book Rating</b>')

# Calculate the correlation matrix using the filtered dataset
correlation_matrix_filtered = filtered_bookrec[['age', 'book_rating', 'year_pub']].corr()

# Create a correlation heatmap using the filtered dataset
fig_heatmap_filtered = go.Figure(go.Heatmap(
    z=correlation_matrix_filtered.values,
    x=correlation_matrix_filtered.columns,
    y=correlation_matrix_filtered.columns,
    colorscale='Viridis',
    colorbar=dict(title='Correlation')
))

# Creating a 3D scatter plot using the filtered dataset
fig_3d_scatter_filtered = px.scatter_3d(filtered_bookrec, x='age', y='book_rating', z='year_pub',
                                        title="<b>3D Scatter Plot</b>", color_discrete_sequence=['#FF7F50'])
fig_3d_scatter_filtered.update_layout(height=600, width=1000, template=custom_template,
                                        scene=dict(xaxis_title='<b>Age</b>', yaxis_title='<b>Book Rating</b>', zaxis_title='<b>Year Published</b>'))


# Creating the streamlit layout
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ['**Age Distribution**', '**Top 10 Locations**', '**Top 10 Rated Books**', '**Top 10 Rated Authors**',
     '**Rating Distribution**', '**User Age Vs User Rating**', '**Correlation Heatmap**', '**3D Scatter Plot**'])

with tab1:
    st.header('Age Distribution')
    st.write(
        f'In this plot, it is possible to observe the presence of outliers. The ages **around and over 70** are most likely erroneous data inputs. These errors may have been made by accident or on purpose. For instance, some users may not want to disclose their personal information.')
    st.plotly_chart(fig_age_filtered)

with tab2:
    st.header('Top 10 Locations')
    st.write(f'Here, it can be seen that the locations with the highest number of individual ratings for books are either in the **USA** or **Canada**.')
    st.plotly_chart(fig_lmr_filtered)

with tab3:
    st.header('Top 10 Rated Books')
    st.write(
        f'This third graph shows the top 10 books with the highest number of individual ratings. It is possible to see that **Wild Animus**, the top-rated, has more than double the number of ratings than the second position, **The Lovely Bones: A Novel**.')
    st.plotly_chart(fig_mrb_filtered)

with tab4:
    st.header('Top 10 Rated Authors')
    st.write(f'In this case, the plot shows the top 10 authors with the highest number of individual ratings, being **Stephen King**, the top-rated.')
    st.plotly_chart(fig_mra_filtered)

with tab5:
    st.header('Rating Distribution')
    st.write(f'The last histogram is about the rating distribution.')
    st.plotly_chart(fig_br_filtered)

with tab6:
    st.header('User Age vs. Book Rating')
    st.write('This scatter plot shows the relationship between user age and book ratings.')
    st.plotly_chart(fig_scatter_filtered)

with tab7:
    st.header('Correlation Heatmap')
    st.write('This heatmap shows the correlation between age, book rating, and publication year.')
    st.plotly_chart(fig_heatmap_filtered)

with tab8:
    st.header('3D Scatter Plot')
    st.write('This 3D scatter plot shows the relationship between age, book rating, and publication year.')
    st.plotly_chart(fig_3d_scatter_filtered)
