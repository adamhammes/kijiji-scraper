[kijiji-scraper](http://kijijimap.hammes.io/)
-------------

`kijiji-scraper` is a tool I used to search for apartments while moving to Quebec.
The program scrapes Kijiji (the local Craigslist equivalent) for apartments on sale and plots them on a map with several options for filtering/favoriting.

The code is split into two parts:

1. The scraper crawls the Kijiji results and cleans/validates the data, finishing by exporting the results to Amazon s3 and to a local json file.
2. The frontend takes the json file and spits out an `index.html` as well as some static resources.
The output of `yarn build` can be served as a static site.

