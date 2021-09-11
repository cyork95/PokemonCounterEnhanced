import cv2
import numpy as np
import urllib.request
import time

regular_url = 'https://www.serebii.net/swordshield/pokemon/'
shiny_url = 'https://www.serebii.net/Shiny/SWSH/'
regular_folder = 'resources/pokemon_images/'
shiny_folder = 'resources/pokemon_shiny_images/'


def image_scraper(url, folder_string, range_x=1, range_y=899):
    start_time = time.time()
    for i in range(range_x, range_y):
        try:
            number_format = '{:03d}'.format(i)
            full_url = url + number_format + '.png'
            request = urllib.request.Request(full_url)
            response = urllib.request.urlopen(request)
            binary_str = response.read()
            byte_array = bytearray(binary_str)
            numpy_array = np.asarray(byte_array, dtype='uint8')
            image = cv2.imdecode(numpy_array, cv2.IMREAD_UNCHANGED)
            cv2.imwrite(folder_string + str(i) + ".png", image)
            print("Saved: " + str(i) + ".png")
        except Exception as e:
            print(str(e))
    end_time = time.time()
    print("Done")
    print("Time taken: " + str(end_time - start_time) + "sec")


print("----------Regular Pokemon Image Scrape Starting----------")
image_scraper(regular_url, regular_folder)
print("----------Regular Pokemon Image Scrape Done----------")
print("----------Shiny Pokemon Image Scrape Starting----------")
image_scraper(shiny_url, shiny_folder)
print("----------Shiny Pokemon Image Scrape Done----------")
