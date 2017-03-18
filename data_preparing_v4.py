import pandas as pd
import numpy as np

from google.cloud import storage
from StringIO import StringIO
from PIL import Image
from sklearn import preprocessing


PROJECT_NAME = 'painting-classifier'
BUCKET_NAME = 'painting-classifier-data'

bucket = storage.Client(project = PROJECT_NAME).bucket(BUCKET_NAME)


def get_image_data(image_path):
	im = Image.open(StringIO(bucket.blob(image_path).download_as_string()))
	return np.array(im.getdata(), dtype = np.float32).reshape(1, im.height, im.width, -1) + np.zeros((1, 1, 1, 3))


def get_resized_img_colors(file_list, image_dir):
	#CURSOR_UP_ONE = '\x1b[1A'
	ERASE_LINE = '\x1b[2K'
	images = []
	format_str = ERASE_LINE + '\rLoading images: %d/%d'
	total_imgs = len(file_list)
	processed = 0
	for img in file_list:
		try:
			img_pixels = get_image_data('resized_200/' + img)
			images.append(img_pixels)
			processed += 1
			sys.stdout.write(format_str % (processed, total_imgs))
			sys.stdout.flush()	
		except BaseException as e:
			sys.stderr.write('Error Loading Image %s\n%s\n' % (img, e))
			sys.stderr.flush()

		sys.stdout.write('\n')
		images = np.vstack(images) / 255

		return images


# possibly call it with ['gogh_van', 'rubens']
def get_net_data(painters = None):
	df_data = pd.read_csv('./data/painting_info_clean.csv')

	# pick two author for the simple test
	if painters is not None:
		if isinstance(painters, int):
			painters = list(df_data['short_name'].value_counts()[:painters])
		if isinstance(painters, list):
			df_data = df_data[df_data['short_name'].isin(painters)]

	# get dummies for all the painters
	y = pd.get_dummies(df_data.short_name)
	dummies_cols = y.columns
	y = np.array(y, dtype = np.float32)


	# get images' width & height
	sizes_paintings = pd.read_csv('./data/images_sizes_2325.csv')
	images_stats = np.array(sizes_paintings[['width', 'height']], dtype = np.float32)

	# balance image data: width, height
	scaler = preprocessing.StandardScaler().fit(images_stats)
	images_stats = scaler.transform(images_stats)

	images_colors = get_resized_img_colors(df_data['file_name'], 'data/resized_200/')


	return images_colors, images_stats, y
