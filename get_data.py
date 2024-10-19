import pandas as pd
from typing import Any, Dict, List, Union
import httpx
# from theme import set_theme
import pandas as pd
import time

netherlands_bounds = {
    "lat_min": 50.5,
    "lat_max": 53.5,
    "lon_min": 3.4,
    "lon_max": 7.2
}

URL = 'https://www.marktplaats.nl/lrp/api/search'

Item = Dict[str, Any]


def get_items(game: str, cat_1=31, cat_2=480, offset=0) -> List[Item]:
    query: Dict[str, Union[str, int]] = dict(
        l1CategoryId=31,
        l2CategoryId=480,
        limit=100,
        offset=offset,
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


def get_item_dataframe(searched_items):
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
    for i in range(len(searched_items)):

        item = searched_items[i]

        itemids.append(item['itemId'])
        product_url = "https://link.marktplaats.nl/" + item['itemId']
        product_urls.append(product_url)
        try:
            delivery_value = next(attr['value'] for attr in item['attributes'] if attr['key'] == 'delivery')
        except:
            delivery_value = ''
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
    df['datetime'] = pd.to_datetime(df['dates'], format='mixed')

    # Sort the DataFrame in descending order based on the datetime column
    df_sorted = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)

    # Create a new column with only yyyymmdd values
    df_sorted['datetime'] = df_sorted['datetime'].dt.strftime('%Y%m%d')

    # Filter the dataframe to include only rows within the Netherlands' bounds
    df_netherlands = df[
        (df['latitude'] >= netherlands_bounds['lat_min']) &
        (df['latitude'] <= netherlands_bounds['lat_max']) &
        (df['longitude'] >= netherlands_bounds['lon_min']) &
        (df['longitude'] <= netherlands_bounds['lon_max'])
        ]

    # Load existing data from file
    existing_df = pd.read_csv('data/MP_Items.csv')

    # Append new data to existing data
    updated_df = pd.concat([existing_df, df_netherlands], ignore_index=True)

    # Remove duplicates based on 'Title' column
    updated_df = updated_df.drop_duplicates(subset='item')

    # Save updated data to file
    updated_df.to_csv('data/MP_Items.csv', index=False)

    return df_netherlands


def get_item_dataframe(searched_items):
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
    # df['datetime'] = pd.to_datetime(df['dates'],format='mixed')

    # Sort the DataFrame in descending order based on the datetime column
    # df_sorted = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)

    # Create a new column with only yyyymmdd values
    # df_sorted['datetime'] = df_sorted['datetime'].dt.strftime('%Y%m%d')

    # Filter the dataframe to include only rows within the Netherlands' bounds
    df_netherlands = df[
        (df['latitude'] >= netherlands_bounds['lat_min']) &
        (df['latitude'] <= netherlands_bounds['lat_max']) &
        (df['longitude'] >= netherlands_bounds['lon_min']) &
        (df['longitude'] <= netherlands_bounds['lon_max'])
        ]
    df_netherlands['new_row'] = True

    return df_netherlands


def save_csv(search_term):
    df = get_item_dataframe(get_items(search_term, ))
    df['search_term'] = search_term
    try:
        # Load existing data from file
        existing_df = pd.read_csv('MP_Items_new.csv')
        existing_df['new_row'] = False
        # Append new data to existing data

        updated_df = pd.concat([existing_df, df], ignore_index=True)

        # Remove duplicates based on 'Title' column
        updated_df = updated_df.drop_duplicates(subset='item')
        # Save updated data to file
        updated_df.to_csv('MP_Items_new.csv', index=False)
        print('saved')
    except:
        print('failed')
        df.to_csv('MP_Items_new.csv', index=False)


def main():
    search_terms = ['kowa', 'asahi',
                    'mamiya','pentax',
                    'rolleiflex','rolleicord'
                    'olympus','nikon',
                    'zenith','takumar',
                    'topcon','primo',
                    'nikkormat','nicca','topcoflex',
                    'ihagee','asahiflex','miranda',
                    'pancolar','autocord','kalloflex',
                    'minolta','primoplan','exakta',
                    'yashica','krasnogorsk','edixa','kiev']
    for search_term in search_terms[-1]:
        print(f"Searching for: {search_term}")
        time.sleep(10)
        save_csv(search_term)
    #asahi = get_item_dataframe(get_items('asahi', ))
    #save_csv(asahi)
if __name__ == "__main__":
    main()