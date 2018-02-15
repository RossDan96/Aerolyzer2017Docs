def HorizonDetectionbyStraightLine(self, directory, img_noblur,image):
	img = cv2.blur(img_noblur, (10,10))
	img = cv2.equalizeHist(img)
	img = cv2.equalizeHist(img)
	img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	edges = cv2.Canny(img,150,200) 					
	lines = cv2.HoughLines(edges,1,np.pi/180,10) 	
	print(str(lines))
	for rho,theta in lines[0]:
		#limiting angle so that it is not more than 45 deg or less than -45
	    if (theta > 5.49  or theta < 0.78) or (theta > 2.35 and theta < 3.92): 
		continue
	    a = np.cos(theta)
	    b = np.sin(theta)
	    x0 = a*rho
	    y0 = b*rho
	    x1 = int(x0 + 1000*(-b))
	    y1 = int(y0 + 1000*(a))
	    x2 = int(x0 - 1000*(-b))
	    y2 = int(y0 - 1000*(a))
	    cv2.line(img_noblur,(x1,y1),(x2,y2),(0,255,0),2)
	cv2.imwrite("results/H_"+image,img_noblur)