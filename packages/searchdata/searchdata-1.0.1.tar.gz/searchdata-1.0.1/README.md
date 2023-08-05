# Searchdata Python SDK

SearchData is an API that allows scraping various search engines such as Google, Bing, Yandex, etc. while using rotating proxies to prevent bans. This SDK for Python makes the usage of the API easier to implement in any project you have.

## Installation

Run the following command in the main folder of your project:

```
pip install searchdata
```

## API Key

To use the API and the SDK you will need an API Key. You can get one by registering at [Searchdata](https://app.searchdata.io/register)

## Classes
This SDK provides a class for each search engine from searchdata.io. Here is the list:

| Class                           | Usage                            |
|---------------------------------|----------------------------------|
| SearchdataGoogleSearch          | google searches                  |
| SearchdataBingSearch            | bing searches                    |
| SearchdataYandexSearch          | yandex searches                  |
| SearchdataGoogleAutocomplete    | google autocomplete searches     |
| SearchdataGoogleEvents          | google events searches           |
| SearchdataGoogleJobs            | google jobs searches             |
| SearchdataGoogleJobsListing     | google jobs listing searches     |
| SearchdataGoogleMaps            | google maps searches             |
| SearchdataGoogleMapsReviews     | google maps reviews searches     |
| SearchdataGoogleProduct         | google product searches          |
| SearchdataGoogleReverseImage    | google reverse image searches    |
| SearchdataGoogleScholar         | google scholar searches          |
| SearchdataGoogleScholarAuthor   | google scholar author searches   |
| SearchdataGoogleScholarCite     | google scholar cite searches     |
| SearchdataGoogleScholarProfiles | google scholar profiles searches |
| SearchdataLocations             | locations api                    |

## Usage

Using the SDK it's quite easy. An example of a GET call to the API is the following:

```
from searchdata import SearchdataLocations, SearchdataGoogleSearch

searchdataGoogleSearch = SearchdataGoogleSearch('YOUR_API_KEY')
locationsAPI = SearchdataLocations()

response = locationsAPI.execute("Austin", 1)
locations = response.json()
location = locationsAPI.process_location(locations[0])
searchdataGoogleSearch.set_q("Test")
searchdataGoogleSearch.set_location(location)
searchdataGoogleSearch.set_lr('lang_en|lang_ar')
response = searchdataGoogleSearch.execute()

# print(response.status_code)
# print(response.headers);
print(response.json());
```

Alternatively, you can use the function executeRaw, which will allow you to send the parameters in an associative array:

```
from searchdata import SearchdataLocations, SearchdataGoogleSearch

searchdataGoogleSearch = SearchdataGoogleSearch('YOUR_API_KEY')
locationsAPI = SearchdataLocations()

response = locationsAPI.execute("Austin", 1)
locations = response.json()
location = locationsAPI.process_location(locations[0])
response = searchdataGoogleSearch.executeRaw({
    'q': 'test',
    'device': 'mobile',
    'lr': 'lang_en|lang_ar',
    'location': location
})

# print(response.status_code)
# print(response.headers);
print(response.json());
```

For a better understanding of the parameters, please check out [our documentation](https://app.searchdata.io/documentation/getting-started).