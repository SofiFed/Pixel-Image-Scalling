def SortPixels(pixels):
	result_pixels = []
	
	for i in range(0,7,3):
		for j in range(i,i+3):
			for k in range(2):
				result_pixels.append(pixels[j][k])
		for j in range(i,i+3):
			for k in range(2,4):
				result_pixels.append(pixels[j][k])
	return result_pixels

def Method_3x3(Method, image, row, col):

	print(f'Start {Method.__name__}')
	width = image.size[0]
	original_pixels = OriginalPixels(image, row, col)
	index = (row-1)*width + (col-1)

	converted_pixels = []

	for obj in original_pixels:
		if obj is not None:
			pixel, index = obj
			converted_pixels.append(Method(image, index))
		else:
			converted_pixels.append((None,)*4)

	return SortPixels(converted_pixels)

def OriginalPixels(image, row=None, col=None, allpixels=True, index=None):

	width = image.size[0]
	height = image.size[1]

	original_pixels = list(image.getdata())
	if index is None:
		index = (row-1)*width + (col-1)

	top = index >= width
	left = index % width
	right = (index+1) % width
	lower = index < width * (height - 1)

	try:
		p2 = (original_pixels[index-width], index-width) if top else None
	except IndexError:
		p2 = None
	try:
		p4 = (original_pixels[index-1], index-1) if left else None
	except IndexError:
		p4 = None
	p5 = (original_pixels[index], index)
	try:
		p6 = (original_pixels[index+1], index+1) if right else None
	except IndexError:
		p6 = None
	try:
		p8 = (original_pixels[index+width], index+width) if lower else None
	except IndexError:
		p8 = None
	
	if allpixels:
		try:
			p1 = (original_pixels[index-width-1], index-width-1) if top and left else None
		except IndexError:
			p1 = None
		try:
			p3 = (original_pixels[index-width+1], index-width+1) if top and right else None
		except IndexError:
			p3 = None
		try:
			p7 = (original_pixels[index+width-1], index+width-1) if left and lower else None
		except IndexError:
			p7 = None
		try:
			p9 = (original_pixels[index+width+1], index+width+1) if right and lower else None
		except IndexError:
			p9 = None
	
	return (p1, p2, p3, p4, p5, p6, p7, p8, p9) if allpixels else (p2, p4, p5, p6, p8)










