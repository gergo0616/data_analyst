from yelpapi import YelpAPI
import pandas as pd

from yelpapi import YelpAPI
import pandas as pd
import time

def get_restaurant_data(api_key, location, limit=50, total_limit=200):
    yelp_api = YelpAPI(api_key)
    
    all_restaurants = []
    offset = 0
    
    while len(all_restaurants) < total_limit:
        try:
            response = yelp_api.search_query(
                term='restaurants',
                location=location,
                limit=limit,
                offset=offset
            )
            
            restaurants = response['businesses']
            
            if not restaurants:
                break
            
            all_restaurants.extend(restaurants)
            offset += len(restaurants)
            
            # Respect Yelp API rate limits
            time.sleep(0.25)  # 250ms delay between requests
            
        except Exception as e:
            print(f"An error occurred while fetching data for {location}: {str(e)}")
            break
    
    if not all_restaurants:
        print(f"No restaurants found for location: {location}")
        return pd.DataFrame()
    
    data = []
    for restaurant in all_restaurants[:total_limit]:
        data.append({
            'name': restaurant['name'],
            'rating': restaurant['rating'],
            'reviews': restaurant['review_count'],
            'price': restaurant.get('price', 'N/A'),
            'categories': ', '.join([category['title'] for category in restaurant['categories']]),
            'address': ', '.join(restaurant['location']['display_address'])
        })
    
    return pd.DataFrame(data)