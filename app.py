import streamlit as st
import pandas as pd
from typing import Any, Dict, List, Set, Union
from contextlib import contextmanager
from pathlib import Path
from openai import OpenAI
import openai
import httpx
import pydeck as pdk
from theme import set_theme

# Call set_theme function
set_theme()
# import telegram
# import config
# from marktplaats import SearchQuery, SortBy, SortOrder

import pandas as pd

netherlands_bounds = {
    "lat_min": 50.5,
    "lat_max": 53.5,
    "lon_min": 3.4,
    "lon_max": 7.2
}

URL = 'https://www.marktplaats.nl/lrp/api/search'
Item = Dict[str, Any]


def get_items(game: str, cat_1=31, cat_2=480) -> List[Item]:
    query: Dict[str, Union[str, int]] = dict(
        l1CategoryId=cat_1,
        l2CategoryId=cat_2,
        limit=100,
        offset=0,
        query=game,
        searchInTitleAndDescription="true",
        viewOptions="list-view",
    )
    resp = httpx.get(URL, params=query)
    resp.raise_for_status()
    return resp.json()['listings']


def format_item(item: Item) -> str:
    price = item['priceInfo'].get('priceCents', 0) / 100
    lines = [
        item['title'],
        str(price) + ' ' + item['priceInfo'].get('priceType', ''),
        item['date'],
        item['location'].get('cityName', ''),
        'https://www.marktplaats.nl' + item['vipUrl'],
    ]
    return '\n'.join(lines)


URL = 'https://www.marktplaats.nl/lrp/api/search'
Item = Dict[str, Any]


def get_item_title(searched_items):
    itemids = []
    titles = []
    image_urls = []
    product_urls = []
    locations = []
    prices = []
    delivery_types = []
    latitudes = []
    longitudes = []
    dates = []
    extended_attributes = []
    seller_names = []
    description = []
    for i in range(len(searched_items)):

        item = searched_items[i]

        itemids.append(item['itemId'])
        product_url = "https://link.marktplaats.nl/" + item['itemId']
        product_urls.append(product_url)
        try:
            delivery_value = next(attr['value'] for attr in item['attributes'] if attr['key'] == 'delivery')
        except:
            delivery_value = ''

        try:
            description_value = item['description']
        except:
            description_value = ''
        description.append(description_value)
        delivery_types.append(delivery_value)
        price = item['priceInfo']['priceCents'] / 100  # Convert from cents to euros
        latitude = item['location']['latitude']
        longitude = item['location']['longitude']
        titles.append(item['title'])
        extended_attributes.append(item['extendedAttributes'][0]['value'])
        seller_names.append(item['sellerInformation']['sellerName'])
        dates.append(item['date'])
        try:
            img = item['pictures'][0]['mediumUrl']
            image_urls.append(img)
        except:
            image_urls.append('https://fotohandeldelfshaven.b-cdn.net/wp-content/uploads/2024/02/52301.jpg')

        latitudes.append(latitude)
        longitudes.append(longitude)
        prices.append(price)

    data = {
        'item': itemids,  # Changed 'Item' to 'item' to match the column name in the existing DataFrame
        'title': titles,
        'description': description,
        'img_url': image_urls,
        'product_url': product_urls,
        'latitude': latitudes,
        'longitude': longitudes,
        'price': prices,
        'delivery': delivery_types,
        'dates': dates,
        'extended_attributes': extended_attributes,
        'seller_names': seller_names

    }
    df = pd.DataFrame(data)

    # Convert the datetime column to datetime format
    #df['datetime'] = pd.to_datetime(df['dates'], format='mixed')

    # Sort the DataFrame in descending order based on the datetime column
    #df_sorted = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)

    # Create a new column with only yyyymmdd values
    #df_sorted['datetime'] = df_sorted['datetime'].dt.strftime('%Y%m%d')

    # Filter the dataframe to include only rows within the Netherlands' bounds
    df_netherlands = df[
        (df['latitude'] >= netherlands_bounds['lat_min']) &
        (df['latitude'] <= netherlands_bounds['lat_max']) &
        (df['longitude'] >= netherlands_bounds['lon_min']) &
        (df['longitude'] <= netherlands_bounds['lon_max'])
        ]

    return df_netherlands


# comment the next function
# comment the next function
# def search_items(search_query):
#     search = SearchQuery(search_query, # Search query
#                         zip_code="2628ZP", # Zip code to base distance from
#                         distance=100000, # Max distance from the zip code for listings
#                         price_from=0, # Lowest price to search for
#                         price_to=100, # Highest price to search for
#                         limit=5, # Max listings (page size, max 25)
#                         offset=0, # Offset for listings (page * limit)
#                         sort_by=SortBy.DATE, # DATE, PRICE, LOCATATION, OPTIMIZED
#                         sort_order=SortOrder.DESC) # ASCending or DESCending

#     listings = search.get_listings()
#     titles = []
#     urls = []
#     prices = []
#     image_urls = []
#     locations = []
#     dates = []
#     #latitude
#     for listing in listings:
#         titles.append(listing.title)
#         urls.append(listing.link)
#         locations.append(listing.location)
#         prices.append(listing.price)
#         latitude = searched_items[i]['location']['latitude']
#         longitude = searched_items[i]['location']['longitude']
#         if len(listing.images) > 0:
#             image_urls.append(listing.images[0].medium)
#         else:
#             image_urls.append('https://fotohandeldelfshaven.b-cdn.net/wp-content/uploads/2024/02/52301.jpg')

#     data = {
#             'Title': titles,
#             'img_url': image_urls,
#             'product_url': urls,
#             'location':locations,
#             'price':prices,

#         }
#     df = pd.DataFrame(data)
#     return df


client = openai.OpenAI(api_key='')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content


# Sample DataFrame


# Streamlit app
def main():
    st.title("Product Gallery")

    # Text area for description input
    searched_items = st.text_area("Description", '')
    cat1 = st.text_input("Enter a number", value="31")
    cat1 = int(cat1)
    cat2 = st.text_input("Enter a number", value="480")
    cat2 = int(cat2)
    # Session state initialization
    if 'df' not in st.session_state:
        st.session_state.df = None

    # Get Items button
    if st.button("Get Items"):
        st.session_state.df = get_item_title(get_items(searched_items, cat_1=cat1, cat_2=cat2))
        st.session_state.df = st.session_state.df.sort_values(by='dates', ascending=False).reset_index(drop=True)

    # Display the gallery if df is available in session state
    if st.session_state.df is not None:
        df = st.session_state.df

        # Multi-select filter for delivery
        delivery_filter = st.multiselect("Filter by Delivery", df['delivery'].unique())

        # Range filter for price
        price_range = st.slider("Filter by Price Range", float(df['price'].min()), float(df['price'].max()),
                                (float(df['price'].min()), float(df['price'].max())))

        # Apply filters
        filtered_df = df[
            df['delivery'].isin(delivery_filter) & (df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]

        #df = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)
        #df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d')
        num_cols = 5
        columns = st.columns(num_cols)
        if st.button("Save DataFrame"):
            df.to_csv('data/dataframe.csv', index=False)
            st.success("DataFrame saved successfully!")
        # Create a map
        st.map(df[['latitude', 'longitude']])
        # Display product images in a gallery
        for index, row in df.iterrows():
            col = columns[index % num_cols]
            with col:
                st.image(row['img_url'], caption=row['title'], use_column_width=True)
                st.write(f"<b>{row['price']}</b>", unsafe_allow_html=True)
                # st.write(row['product_url'])
                #st.write(row['datetime'])
                # st.write(row['datetime'].split()[0])
                # st.markdown(row['datetime'], unsafe_allow_html=True)
                st.markdown(f"<a href='{row['product_url']}' target='_blank'>View</a>", unsafe_allow_html=True)

def page_live_searchterms():
    # df = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)
    # df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d')
    # Add 'All' option to show all items
    search_terms = ['All','kowa','asahi',
                    'mamiya','pentax',
                    'rolleiflex','rolleicord',
                    'olympus','nikon',
                    'zenith','takumar',
                    'topcon','primo',
                    'nikkormat','nicca','topcoflex',
                    'ihagee','asahiflex','miranda',
                    'pancolar','autocord','kalloflex',
                    'minolta','primoplan','exakta',
                    'yashica','krasnogorsk','edixa','kiev']
    # add radio buttons for search terms
    selected_term = st.sidebar.radio("Select Search Terms", search_terms)
    # Display items based on selected search term
    cat1 = st.text_input("Enter a number", value="31")
    cat1 = int(cat1)
    cat2 = st.text_input("Enter a number", value="480")
    cat2 = int(cat2)
    # Get Items button
    if selected_term!= 'All':
        st.session_state.df = get_item_title(get_items(selected_term, cat_1=cat1, cat_2=cat2))
        st.session_state.df = st.session_state.df.sort_values(by='dates', ascending=False).reset_index(drop=True)
    else:
        st.session_state.df = get_item_title(get_items(' ', cat_1=cat1, cat_2=cat2))
        st.session_state.df = st.session_state.df.sort_values(by='dates', ascending=False).reset_index(drop=True)

    # Display the gallery if df is available in session state
    if st.session_state.df is not None:
        df = st.session_state.df

        num_cols = 5
        columns = st.columns(num_cols)
        # Create a map
        st.map(df[['latitude', 'longitude']])
        # Display product images in a gallery
        for index, row in df.iterrows():
            col = columns[index % num_cols]
            with col:
                st.image(row['img_url'], caption=row['title'], use_column_width=True)
                st.write(f"<b>{row['price']}</b>", unsafe_allow_html=True)
                # st.write(row['product_url'])
                # st.write(row['datetime'])
                # st.write(row['datetime'].split()[0])
                # st.markdown(row['datetime'], unsafe_allow_html=True)
                st.markdown(f"<a href='{row['product_url']}' target='_blank'>View</a>", unsafe_allow_html=True)


def page2():
    st.title("Product Gallery")

    # Load data from a CSV file (replace 'MP_Items_new.csv' with the actual file path)
    df = pd.read_csv('MP_Items_new.csv')

    # Get the unique values for each search term, converted to lowercase
    unique_search_terms = df['search_term'].str.lower().unique()

    # Add 'All' option to show all items
    search_terms = [' ','All','kowa','asahi',
                    'mamiya','pentax',
                    'rolleiflex','rolleicord',
                    'olympus','nikon',
                    'zenith','takumar',
                    'topcon','primo',
                    'nikkormat','nicca','topcoflex',
                    'ihagee','asahiflex','miranda',
                    'pancolar','autocord','kalloflex',
                    'minolta','primoplan','exakta',
                    'yashica','krasnogorsk','edixa','kiev']

    # Order search terms alphabetically
    search_terms.sort()

    # Create horizontal radio buttons using st.columns
    cols = st.columns(len(search_terms))
    selected_category = None
    for i, term in enumerate(search_terms):
        if cols[i].button(term.capitalize()):  # Capitalize the search terms for better display
            selected_category = term

    # Default to "All" if no button has been selected
    if selected_category is None:
        selected_category = 'all'

    # Filter the DataFrame based on the selected category
    if selected_category == 'all':
        filtered_df = df  # Show all items if 'All' is selected
    else:
        filtered_df = df[df['search_term'] == selected_category]

    # Sort by date (or any other sorting condition)
    filtered_df = filtered_df.sort_values(by='dates', ascending=False).reset_index(drop=True)

    # Display the gallery if data is available
    if not filtered_df.empty:
        num_cols = 5
        columns = st.columns(num_cols)
        for index, row in filtered_df.iterrows():
            col = columns[index % num_cols]
            with col:
                st.image(row['img_url'], caption=row['title'], use_column_width=True)
                st.write(f"<b>{row['price']}</b>", unsafe_allow_html=True)
                st.markdown(f"<a href='{row['product_url']}' target='_blank'>View</a>", unsafe_allow_html=True)
    else:
        st.write("No items found.")


# Streamlit app
if __name__ == "__main__":
    pages = {
        "Live Search Terms": page_live_searchterms,
        "Live Search": main,

        "From Data": page2
    }

    st.sidebar.title("Navigation")
    selection = st.radio("Go to", list(pages.keys()))

    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
