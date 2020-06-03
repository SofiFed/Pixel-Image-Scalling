import tkinter as tk 
from tkinter import filedialog, messagebox
from tkinter.font import Font
from tkinter.ttk import Progressbar
from webcolors import rgb_to_hex 
from PIL import Image, ImageTk
import numpy as np

from PixelMethods import OriginalPixels, Method_3x3
from ScalingMethods1Pixel import FDM, FEM, AdvMAME2x

window = tk.Tk()
window.title('Pixel Image Scalling')
w = window.winfo_screenwidth()//2 - 555
window.geometry(f'1110x660+{w}+10')
window.iconphoto(True, tk.PhotoImage(file='icon.gif'))

canvas = tk.Canvas(window)
canvas.pack(fill=tk.BOTH, expand=1)

label1 = tk.Label(window, text='Finite difference method(FDM)', 
	font=("Helvetica", 14)).place(x=510, y=17)
label2 = tk.Label(window, text='Finite element method(FEM)', 
	font=("Helvetica", 14)).place(x=825, y=17)
label3 = tk.Label(window, text='EPX/Scale2x/AdvMAME2x', 
	font=("Helvetica", 14)).place(x=528, y=317)
label4 = tk.Label(window, text='Original pixels', 
	font=("Helvetica", 14)).place(x=835, y=317)

label5 = tk.Label(window, text='row:', 
	font=("Courier", 18)).place(x=990, y=340)
label6 = tk.Label(window, text='column:', 
	font=("Courier", 18)).place(x=990, y=430)

file, image = None, None
spinRow, spinCol = None, None
method1, method2, method3 = None, None, None
original_pixels = None
info_isavailable = False

showimg = tk.Label(window)
size_info1 = tk.Label(window)
size_info2 = tk.Label(window)

def SelectImage():
	global file, info_isavailable
	info_isavailable = False
	file = filedialog.askopenfilename()

	extensions = ['jpg', 'png', 'gif']
	if file.split(".")[-1] not in extensions:
		file = None
		errortext = "The image must have the extension .png, .jpg or .gif!"
		messagebox.showerror('Error', errortext) 
	else:
		ClearFields()
		ShowImage(file)

getimage_button = tk.Button(window, text="select an image...", 
	bg="#c78fff", font=("Courier", 12, 'bold'), command=SelectImage, 
	width=44).place(x=30, y=5)

def EmptyImage(color):
	canvas.create_rectangle(30, 45, 480, 581, 
      outline=color, fill=color)

def ShowImage(file):
	global image, showimg, size_info1, size_info2, spinRow, spinCol
	Original(["#ac74e3"]*9)

	image = None
	showimg.image = None

	max_width, max_height = 448, 534
	image = Image.open(file)
	img = image
	img_width, img_height = img.size[0], img.size[1]
	cut = 0
	while True:
		new_width = max_width - cut
		new_height = int(new_width * img.size[1] / img.size[0])
		if new_height > max_height:
			new_height = max_height - cut
			new_width = int(new_height * img.size[0] * img.size[1])
		if new_width < max_width and new_height < max_height:
			break
		else:
			cut += 1

	x, y = 30, 45
	if new_height > new_width:
		x += int((max_width - new_width)/2)
	else:
		y += int((max_height - new_height)/2)

	img = img.resize((new_width, new_height), Image.ANTIALIAS)

	render = ImageTk.PhotoImage(img)
	EmptyImage('#ffffff')
	showimg = tk.Label(window, image=render, bg="#ffffff")
	showimg.image = render
	showimg.place(x=x, y=y)

	text_size1 = f'The size of original image: {img_width} x {img_height}'
	size_info1 = tk.Label(window, text=text_size1, 
		font=("Courier", 13), width=45).place(x=30, y=585)

	text_size2 = f'The size of new image: {2*img_width} x {2*img_height}'
	size_info2 = tk.Label(window, text=text_size2, 
		font=("Courier", 13), width=45).place(x=30, y=610)

	spinRow = tk.Spinbox(window, from_=1, to=img_height, width=5, 
		font=Font(family='Helvetica', size=18, weight='bold'))
	spinRow.place(x=995, y=380)
	spinCol = tk.Spinbox(window, from_=1, to=img_width, width=5, 
		font=Font(family='Helvetica', size=18, weight='bold'))
	spinCol.place(x=995, y=470)

	startmethods_button = tk.Button(window, text="start scaling process", bg="#c78fff", 
		font=("Courier", 12), command=StartMethods, width=26).place(x=810, y=540)

	savemethods_button = tk.Button(window, text="download information(.txt)", 
		bg="#c78fff", font=("Courier", 12), command=SaveInformation, 
		width=26).place(x=810, y=580)

	#savemethods_button = tk.Button(window, text="scaling completely", 
	#	bg="#c78fff", font=("Courier", 12), command=ImageScaling, 
	#	width=26).place(x=810, y=620)

def StartMethods():
	global original_pixels, method1, method2, method3
	global info_isavailable
	ClearFields()
	try:
		row = int(spinRow.get())
		col = int(spinCol.get())
		if not 1 <= row <= image.size[1] or not 1 <= col <= image.size[0]:
			raise Exception
	except:
		errortext = "Values are not correct! Re-enter, please."
		errortext += f"\nValue of row must be from 1 to {image.size[1]}"
		errortext += f"\nValue of column must be from 1 to {image.size[0]}"
		messagebox.showerror('Error', errortext) 
	else:
		messagebox.showinfo('Start Scaling Process', 
		'Scaling process will take some time') 
			
		original_pixels = [i[0] if i is not None else None 
			for i in OriginalPixels(image, row, col)]
		method1 = Method_3x3(FDM, image, row, col)
		method2 = Method_3x3(FEM, image, row, col)
		method3 = Method_3x3(AdvMAME2x, image, row, col)

		Original(HexColors(original_pixels))
		FirstMethod(HexColors(method1),6)
		SecondMethod(HexColors(method2),6)
		ThirdMethod(HexColors(method3),6)

		info_isavailable = True

def SaveInformation():
	global info_isavailable
	if info_isavailable:
		row = int(spinRow.get())
		col = int(spinCol.get())
		message = f'Do you want to download information\nabout the pixel ({row}; {col}) ?'
		click = messagebox.askokcancel('Download information', message)
		if click:
			def convert(pixel, hsl=False):
				converted = tuple(map(lambda i: int(i), pixel))
				return HSL(converted) if hsl else converted

			def show_result(method):
				return f'\nRGB\n{convert(method[14])} {convert(method[15])}' \
				 	+ f'\n{convert(method[20])} {convert(method[21])}' \
				 	+ f'\nHSL\n{convert(method[14], True)} {convert(method[15], True)}' \
				 	+ f'\n{convert(method[20], True)} {convert(method[21], True)}' \

			textfile = f'Image file {file.split("/")[-1]}' \
				 + f'\nOriginal size: {image.size[0]}x{image.size[1]}' \
				 + f'\n\nPixel row: {row}, column: {col}' \
				 + f'\nOriginal color: \nRGB {original_pixels[4]}' + f'\nHSL {HSL(original_pixels[4])}' \
				 + '\n\nFinite difference method:' + show_result(method1) \
				 + '\n\nFinite element method:' + show_result(method2) \
				 + '\n\nEPX/Scale2x/AdvMAME2x:' + show_result(method3) 
			
			image_text = open(f'{file.split("/")[-1]}_pixel_{row}_{col}.txt', 'w')
			image_text.write(textfile)
			image_text.close()
	else:
		messagebox.showerror('Error', 'You must scale the pixel before loading the information!') 


def Field(startX, startY, size, pixels, original=False):
	length = 90 if size == 3 else 45
	length = 58 if original else length
	for i in range(size):
		for j in range(size):
			canvas.create_rectangle(startX+length*j, startY+length*i, 
				startX+length*(j+1), startY+length*(i+1),
	      		outline=pixels[i*size+j], fill=pixels[i*size+j])
			if not pixels[i*size+j]:
				canvas.create_rectangle(startX+length*j, startY+length*i,
					startX+length*(j+1), startY+length*(i+1), fill='#ffffff')
				canvas.create_rectangle(startX+length/3+length*j, 
					startY+length/3+length*i, startX-length/3+length*(j+1), 
					startY-length/3+length*(i+1), fill="#000000")

	for i in range(size+1):
		canvas.create_line(startX+length*i, startY,
			startX+length*i, startY+length*size)
		canvas.create_line(startX, startY+length*i,
			startX+length*size, startY+length*i)

def ImageScaling():
	global image
	method = FEM
	original_image = image
	width = original_image.size[0]
	height = original_image.size[1]

	original_pixels = list(original_image.getdata())
	converted_pixels = []

	for index, pixel in enumerate(original_pixels):
		print(index)
		converted_pixels.append(method(image, index))

	result_pixels = []
	for i in range(height):
		result_pixels.append([])
		for j in range(width):
			result_pixels[-1].append(converted_pixels[j + width*i][0])
			result_pixels[-1].append(converted_pixels[j + width*i][1])
		result_pixels.append([])
		for j in range(width):
			result_pixels[-1].append(converted_pixels[j + width*i][2])
			result_pixels[-1].append(converted_pixels[j + width*i][3])

	pixels_array = np.array(result_pixels, dtype=np.uint8)
	result_image = Image.fromarray(pixels_array)
	result_image.save(f"new_by_{method.__name__}.jpg")

def HexColors(pixels):
	hexpixels = []
	for pixel in pixels:
		if pixel is None:
			hexpixels.append(None)
		else:
			hexpixels.append(rgb_to_hex([int(i) for i in pixel]))
	return hexpixels

def HSL(rgb):
	R, G, B = rgb[0] / 255, rgb[1] / 255, rgb[2] / 255
	MIN, MAX = min(R, G, B), max(R, G, B)
	L = (MIN + MAX) / 2
	S = (MAX - MIN) / (1 - abs(1 - MAX - MIN))

	if MAX == MIN:
		H = None
	elif MAX == R and G >= B:
		H = 60*(G - B)/(MAX - MIN) + 0
	elif MAX == R and G < B:
		H = 60*(G - B)/(MAX - MIN) + 360
	elif MAX == G:
		H = 60*(B - R)/(MAX - MIN) + 120
	elif MAX == B:
		H = 60*(R - G)/(MAX - MIN) + 240

	return f"({'%.2f' % H}, {'%.2f' % S}%, {'%.2f' % L}%)"

def FirstMethod(pixels, size=3):
	Field(510,45,size, pixels)

def SecondMethod(pixels, size=3):
	Field(810,45,size, pixels)

def ThirdMethod(pixels, size=3):
	Field(510, 345, size, pixels)

def Original(pixels):
	Field(810, 345, 3, pixels, True)

def ClearFields():
	Original(["#ac74e3"]*9)
	FirstMethod(["#ac74e3"]*9)
	SecondMethod(["#ac74e3"]*9)
	ThirdMethod(["#ac74e3"]*9)

EmptyImage("#d7b8f5")
ClearFields()

window.mainloop()