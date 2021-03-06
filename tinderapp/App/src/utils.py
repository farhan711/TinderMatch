from __future__ import division
import operator
from PIL import Image
from collections import deque
from Region import *
from Pixel import *

def create_skin_regions(pixels, skin_pixels, skin_regions, width, height):
    for i in xrange(0, width):
        for j in xrange(0, height):
            pixel = pixels[i][j]
            if pixel.is_skin() and not pixel.in_region():
                region = Region()
                skin_regions.append(region)
                pixel_queue = deque()
                pixel_queue.append(pixel)
                breadth_first_skin_search(pixels, skin_pixels, region, pixel_queue, width, height)

# TODO : Fairly slow, any improvements possible?
def breadth_first_skin_search(pixels, skin_pixels, region, pixel_queue, width, height):
    while not len(pixel_queue) == 0:
        pixel = pixel_queue.popleft()
        if pixel.is_skin() and not pixel.in_region():
            pixel.region = region
            region.add_pixel(pixel)
            skin_pixels.append(pixel)
            for i in xrange(-1, 2):
                for j in xrange(-1, 2):
                    x, y = pixel.x + i, pixel.y + j
                    if 0 <= x < width and 0 <= y < height:
                        pixel_queue.append(pixels[x][y])

# Return < 0 if "left" of line
# 0 if on line, > 0 if "right" of line
def side_of_line(start_pixel, end_pixel, pixel):
    start_x = start_pixel.x
    start_y = start_pixel.y
    end_x = end_pixel.x
    end_y = end_pixel.y
    return ((end_x - start_x) * (pixel.y - start_y) -((end_y - start_y) * (pixel.x - start_x)))

def inside_bounding_region(topmost_pixel, bottommost_pixel, rightmost_pixel, leftmost_pixel, pixel):
    inside_region = (side_of_line(leftmost_pixel, topmost_pixel, pixel) >= 0)
    inside_region = inside_region and (side_of_line(topmost_pixel, rightmost_pixel, pixel) >= 0)
    inside_region = inside_region and (side_of_line(rightmost_pixel, bottommost_pixel, pixel) >= 0)
    inside_region = inside_region and (side_of_line(bottommost_pixel, leftmost_pixel, pixel) >= 0)
    return inside_region

# Create bounding region as per algorithm
# Based on polygon created by four points
def create_bounding_region(pixels, skin_regions, width, height):
    bounding_region = Region()
    topmost_points_list = []
    bottommost_points_list = []
    rightmost_points_list = []
    leftmost_points_list = []
    for i in xrange(0, 3):
        topmost_points_list.append(skin_regions[i].topmost_pixel())
        bottommost_points_list.append(skin_regions[i].bottommost_pixel())
        leftmost_points_list.append(skin_regions[i].leftmost_pixel())
        rightmost_points_list.append(skin_regions[i].rightmost_pixel())

    topmost_points_list.sort(key = operator.attrgetter('x'), reverse=False)
    bottommost_points_list.sort(key = operator.attrgetter('x'), reverse=True)
    rightmost_points_list.sort(key = operator.attrgetter('y'), reverse=False)
    leftmost_points_list.sort(key = operator.attrgetter('y'), reverse=True)

    topmost_pixel = topmost_points_list[0]
    bottommost_pixel = bottommost_points_list[0]
    rightmost_pixel = rightmost_points_list[0]
    leftmost_pixel = leftmost_points_list[0]

    for i in xrange(0, width):
        for j in xrange(0, height):
            pixel = pixels[i][j]
            if inside_bounding_region(topmost_pixel, bottommost_pixel, rightmost_pixel, leftmost_pixel, pixel):
                bounding_region.add_pixel(pixel)
    return bounding_region

def analyze_regions(skin_pixels, skin_regions, bounding_region, width, height):
    skin_pixels_percentage = (len(skin_pixels))/(width * height)
    largest_region_percentage = (skin_regions[0].size)/(width * height)
    skin_in_bounding_polygon_percentage = ((bounding_region.number_of_skin_pixels())/(bounding_region.size)) 
    num_skin_pixels = len(skin_pixels)
    return skin_pixels_percentage
    
#    if skin_pixels_percentage < 0.15:
#        return False
#    if (skin_regions[0].size < (0.35 * num_skin_pixels)) and (skin_regions[1].size < (0.30 * num_skin_pixels)):
#        if skin_regions[2].size < (0.30 * num_skin_pixels):
#            return False
#    if skin_regions[0].size < (0.45 * num_skin_pixels):
#        return False
#    if num_skin_pixels < (0.30 * width * height) and skin_in_bounding_polygon_percentage < 0.55:
#        return False
#    if len(skin_regions) > 60 and bounding_region.average_intensity < (0.25 * 255):
#        return False
#
#    return True

def color_skin_regions(img_path, save_path):
    image = Image.open(img_path)
    pixels = image.load()
    width = image.size[0]
    height = image.size[1]
    
    for i in xrange(0, width):
        for j in xrange(0, height):
            pixel = Pixel(i, j, pixels[i,j][0], pixels[i, j][1], pixels[i, j][2])
            if pixel.is_skin():
                pixels[i, j] = (0, 0, 0)
    image.save(save_path)
