# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import snowflake.connector

# Access secrets
sf_user = st.secrets["snowflake"]["user"]
sf_password = st.secrets["snowflake"]["password"]
sf_account = st.secrets["snowflake"]["account"]
sf_warehouse = st.secrets["snowflake"]["warehouse"]
sf_database = st.secrets["snowflake"]["database"]
sf_schema = st.secrets["snowflake"]["schema"]

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=sf_user,
    password=sf_password,
    account=sf_account,
    warehouse=sf_warehouse,
    database=sf_database,
    schema=sf_schema
)

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# title = st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name of your smoothie will be: ', name_on_order)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your Smoothie!")

session = conn
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5

)

if ingredients_list:
    st.write(ingredients_list)
    st.text(ingredients_list)

    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    # st.write(my_insert_stmt)
    # st.stop()
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your smoothie is ordered, {name_on_order}!', icon='✅')
