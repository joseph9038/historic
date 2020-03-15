# Historic San Francisco

This project is part of an effort to make San Francisco's history more visible to people living in the city. The intent here is to invert what the [San Francisco Historical Society](https://sfhistory.org/) and the [California Historical Society](https://californiahistoricalsociety.org/) aim to do: instead of having history contained in a single building people can visit, disperse digital forms of it around town, tied to their respective locations.

How? Using open source data sets of location-based data, I'm trying to create an augmented reality app that will let people open their phone, point the camera at the city around them, and see digitized historical markers and content overlayed onto their camera's viewport. I'm hoping to eventually assemble my own data sets, but I'm starting with freely available datasets, like this one of [historical San Francisco landmarks](https://data.sfgov.org/dataset/Landmarks/hfwn-m3tm).

## Development

The goal of this project, for me as a software engineer, is to play around with some new frameworks that I don't usually work with. In putting this together, I'm using:

* PostgreSQL, instead of MySQL
* SQLAlchemy, instead of Django's ORM
* Flask, instead of Django
* flask-restx, instead of the Django REST Framework
* vue.js, instead of React
* foundation-sites, instead of Bootstrap

This project is GIS-based, meaning that I'm using it to get some familiarity with GIS systems. In loading data for a user, you have to detect their current location and send those coordinates to a database capable of doing spatial queries from spatially indexed data.

For spatial indexing and querying, I'm using the exceptionally powerful PostGIS extension to PostgreSQL, which allows for querying of N nearest neighbors, or neighbors within a given distance.

For now, I'm attempting to use the wonderful [AR.js JavaScript Framework](https://github.com/jeromeetienne/AR.js) in order to create the augmented reality experience right in the browser. In the long-term I may end up porting this over to be an iOS app using ARKit, but I'm leaning into Atwood's law for the time being.

I'm also refamiliarizing myself with the Google Maps JavaScript API by plotting the landmarks on a map based on user input, an API I haven't worked with in close to a decade.
