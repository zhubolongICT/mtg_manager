import os
from mtg.drawer.GridImagesDrawer import GridImagesDrawer


def test_grid_images_drawer():

    drawer = GridImagesDrawer()
    image_filepath_list = list()
    M21_EN_IMAGES_DIR_PATH = 'data/sets/m21/en/png'

    for i in range(1, 10):
        image_filepath_list.append(
            os.path.join(M21_EN_IMAGES_DIR_PATH, 'm21_%d.png' % i))

    drawer.draw(image_filepath_list, 'test001',
                output_dirpath='grid_images',
                isCardBack=True)


if __name__ == '__main__':
    test_grid_images_drawer()
