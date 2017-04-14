## Data Manipulation

These notebooks detail the essential data manipulation steps taken, after all the web scraping was done.

The files are:

- **`main_data_transformations.ipynb`** contains scripts to find the image sizes, filter out sculptures and other categories, as well as generate the color histograms.
- **`art_movements.ipynb`** contains the code behind the reduction in the amount of art movements, to later be used in models that try to predict the movements.
- **`data_pre_models.ipynb`** contains the code that generates train/test splits and combines data from several sources, aimed at being fed directly into predictive models.
- **`image_resizer.ipynb`** code that resizes all the images in half (in order to speed up their loading during neural network training).
- **`map.ipynb`** code that finds the geolocations for all the paintings and outputs a table with list of cities and number of paintings in each.