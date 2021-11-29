from math import *
from PIL import Image, ImageDraw, ImageFont
import time
import datetime
start = time.time()
# settings that you can easily modify



image_side_len = 2**17

write_numbers_in_cells = True
maximum_digits = 20
digits_to_keep_when_number_is_shortened = 6
font_size = 12

single_cell_size = 170



# end of settings easy to modify
image_dimension = (image_side_len, image_side_len)
colors = {"black": (0, 0, 0), "white":(255, 255, 255), "grey": (100, 100, 100), "almost-white":(240, 240, 240)}
base_margin = [800] * 2
Roboto_font = ImageFont.truetype("Roboto-Medium.ttf", font_size)
width_for_sides = 1
mod_number_to_shorten = 10**digits_to_keep_when_number_is_shortened
max_n_reached = (image_side_len - 2 * base_margin[0]) // single_cell_size - 1

def border_square(img, x, y, cellsize, bm, fill_color, img_dim, side_width):

	draw = ImageDraw.Draw(img)

	chosed_width = side_width

	draw.line([(bm[0] + cellsize * x, bm[1] + cellsize * y), (bm[0] + cellsize * (x+1) - 1, bm[1] + cellsize * y)], fill=fill_color, width=chosed_width)
	draw.line([(bm[0] + cellsize * x, bm[1] + cellsize * (y+1) - 1), (bm[0] + cellsize * (x+1) - 1, bm[1] + cellsize * (y+1) - 1)], fill=fill_color, width=chosed_width)
	draw.line([(bm[0] + cellsize * (x+1) - 1, bm[1] + cellsize * y), (bm[0] + cellsize * (x+1) - 1, bm[1] + cellsize * (y+1) - 1)], fill=fill_color, width=chosed_width)
	draw.line([(bm[0] + cellsize * x, bm[1] + cellsize * y), (bm[0] + cellsize * x, bm[1] + cellsize * (y+1) - 1)], fill=fill_color, width=chosed_width)
	
	return img


def write_in_cell(img, text, x, y, cellsize, write_color, bm):

	draw = ImageDraw.Draw(img)

	ascent, descent = Roboto_font.getmetrics()
	(text_width, text_baseline), (text_offset_x, text_offset_y) = Roboto_font.font.getsize(text)

	draw.text((bm[0] + cellsize * x + (cellsize - text_width) // 2, bm[1] + cellsize * y + (cellsize - (ascent - text_offset_y)) // 2), text, font=Roboto_font, fill=write_color)

	return img


def fill_box(img, x, y, cellsize, bm, fill_color, img_dim):

	draw = ImageDraw.Draw(img)

	draw.rectangle([(bm[0] + cellsize * x + width_for_sides, bm[1] + cellsize * y + width_for_sides), \
		(bm[0] + cellsize * (x+1) - 1 - width_for_sides, bm[1] + cellsize * (y+1) - 1 - width_for_sides)], fill = fill_color )

	return img


if __name__ == "__main__":

	previous_line = [1]
	current_line = []

	img = Image.new(mode = "RGB", size = image_dimension, color = (0, 0, 0))

	for x in range((image_side_len - 2 * base_margin[0]) // single_cell_size):
		for y in range((image_side_len - 2 * base_margin[1]) // single_cell_size):

			if (y <= x):

				comb_factor = 0

				if (y == 0):
					comb_factor = 1
				elif x == y:
					comb_factor = 1
				else:
					comb_factor = previous_line[y - 1] + previous_line[y]

				current_line.append(comb_factor)

				is_even = comb_factor % 2 == 0

				if (len(str(comb_factor)) > maximum_digits):
					comb_factor = "10^" + str(len(str(comb_factor)) - 1) + " + " + str(comb_factor % mod_number_to_shorten)
			
				img = border_square(img, y, x, single_cell_size, base_margin, colors["white"], image_dimension, width_for_sides)

				if is_even:
					fill_box(img, y, x, single_cell_size, base_margin, colors["almost-white"], image_dimension)

				if write_numbers_in_cells:
					color_to_write = "black"
					if is_even:
						color_to_write = "black"
					else:
						color_to_write = "white"
					write_in_cell(img, str(comb_factor), y, x, single_cell_size, colors[color_to_write], base_margin)

		#print(current_line)
		previous_line = current_line
		current_line = []

	#img = border_square(img, 4, 5, single_cell_size, image_dimension)

	#img.show()
	filename = str(datetime.datetime.now()).replace(":", "-") + ".png"
	img.save(filename)

	print(max_n_reached)
	print("Progam ran in {0} seconds".format(round(time.time() - start, 3)))