def Horizon(directory, image, output=0):
	# Read image
	imgOg = cv2.imread(str(directory)+image) 						
	
	# Convert from BGR to YCRCB
	img_YUV = cv2.cvtColor(imgOg,cv2.COLOR_BGR2YCR_CB)

	# Split into blue-green-red channels			
	b, r, g = cv2.split(img_YUV)

	# Equalize Blue Channel & Merge channels back 									
	imgBlueEqu = cv2.merge((cv2.equalizeHist(b), r, g))	

	# Convert from YCRCB to BGR			
	img_BGR = cv2.cvtColor(imgOg,cv2.COLOR_YCR_CB2BGR)				

	# Perform a gaussian blur
	blur = cv2.GaussianBlur(img_BGR,(5,5),0)						

	# Convert to Greyscale
	img_GREY = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)				

	# Threshold image to segment sky
	ret, thresh = cv2.threshold(img_GREY,120,125,cv2.THRESH_BINARY)	

	# Perform erosian and dialiation to isolate the sky
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5), (3,3))
	img_erode = cv2.erode(thresh, kernel)
	img_dilate = cv2.dilate(img_erode, kernel)

	img, contours, hierarchy = cv2.findContours(img_dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

	contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
	if len(contour_sizes) > 0:
		biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
		print "\t"+str(image)+"\t"+str(cv2.contourArea(biggest_contour))+" \t\tPASS"
		if output != 0:
			# Outline elements that may be the sky
			final = cv2.drawContours(imgOg, biggest_contour, -1, (0,255,0), 3)
			# Write to file
			cv2.imwrite(output+"H_"+image,final)					
	else:
		print "\t"+str(image)+"\t\t\tFAIL"