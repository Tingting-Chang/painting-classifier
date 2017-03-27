from sklearn import preprocessing as skprep
import numpy as np
import loading_utils

from preprocessing import (loaders, consumers, operations,
                    Preprocessor, Generator)
import loading_utils

def images_generator_author(num_authors):
    loader = loaders.CSVLoader('data/train_author200.csv', 'data/test_author200.csv')
    prep = Preprocessor()
    prep.with_pipeline('input').set_loader(
            loader.select_loader(['author_id', 'painting_id', 'height_px', 'width_px'])
    prep.add_operation(operations.CategoricalFilter('author_id', top_categories = 3))
    prep.add_operation(loading_utils.HeightWidthRatio()).add_operation(operations.ColumnDrop('height_px', 'width_px'))
    relay = consumers.SimpleDataRelay()
    prep.set_consumer(relay)
    prep.with_pipeline('metadata').set_loader(relay).add_operation(operations.Selector(['height_width_ratio']))
    prep.add_operation(operations.ToNdarray()).add_operation(skprep.StandardScaler())
    response_dummifier = operations.Dummifier() # columns can be recovered by calling response_dummifier.get_output_columns()
    prep.with_pipeline('response').set_loader(relay).add_operation(operations.Selector('author_id'))
    prep.add_operation(prep.response_dummifier).add_operation(operations.ToNdarray())
    prep.with_pipeline('resized_200').set_loader(relay).add_operation(operations.Selector(['author_id', 'painting_id'])
    prep.with_pipeline('full').set_loader(relay).add_operation(operations.Selector(['author_id', 'painting_id'])
    prep.with_pipeline('indices').set_loader(relay).add_operation(operations.Selector(['author_id', 'painting_id'])
    generator = Generator(prep, {'resized_200': loading_utils.ImageLoaderGenerator('resized_200'),
                            'full': loading_utils.ImageLoaderGenerator('full')}, operations.SeparateKey('response'))
    return generator, response_dummifier
