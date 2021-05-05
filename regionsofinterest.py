import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'C:\Users\Pubud\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
from cv2 import cv2
from PIL import Image
import matplotlib.pyplot as plt

im = cv2.imread('page_1_cropped.jpg')

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (9,9), 0)
# thresh2 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,11,30)
thresh2 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Dilate to combine adjacent text contours
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
dilate = cv2.dilate(thresh2, kernel, iterations=4)

# Find contours, highlight text areas, and extract ROIs
cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

line_items_coordinates = []
for c in cnts:
    area = cv2.contourArea(c)
    x,y,w,h = cv2.boundingRect(c)

    weight = 3900
    weight2 = 20
    # print("x,y,w,h",x,y,w,h)
    if area > 10000:
            image = cv2.rectangle(im, (x-weight2,y-weight2), (weight, y+h), color=(255,0,255), thickness=3)
            line_items_coordinates.append([(x-weight2,y-weight2), (weight, y+h)])
    
cv2.imwrite(r'xregionified4.jpg',image)
#-----------
def show_images(titles, images):
    # titles = ['dilate']
    # images = [dilate]
    _range = len(images)

    for i in range(_range):
        plt.subplot(1, 3, i+1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]),plt.yticks([])

    plt.show()
#-----------

################### OCR Part
# load the original image
image = cv2.imread('page_1_cropped.jpg')
image_copy = image
# for i,cord in reversed(list(enumerate(line_items_coordinates))):
for i,cord in reversed(list(enumerate(line_items_coordinates))):
    # get co-ordinates to crop the image
    c = line_items_coordinates[i]

    #Get area to crop ROIs
    length = c[1][0] - c[0][0]
    height = c[1][1] - c[0][1]
    area = length * height

    if (area >= 200000 ):
    # cropping image img = image[y0:y1, x0:x1]
        img = image[c[0][1]:c[1][1], c[0][0]:c[1][0]]    

    # convert the image to black and white for better OCR
    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret1,thresh1 = cv2.threshold(gray2,120,255,cv2.THRESH_BINARY)
    thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    bilf = cv2.bilateralFilter(gray2,9,75,75)

    # titles = ['thresh1','thresh2', 'bilf']
    # images = [thresh1, thresh2, bilf]
    # show_images(titles, images)

    
    # pytesseract image to string to get results
    text = str(tess.image_to_string(thresh2, lang='sin+eng', config='--psm 6'))
    print(text)