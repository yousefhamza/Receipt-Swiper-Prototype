__author__ = 'yousefhamza'

import os
import copy
import sys

import cv2


_cost = 0
_debugging = False

def getSwipedArea(event, x, y, flags, small_receipt):
    global _debugging

    if event == cv2.EVENT_LBUTTONDOWN:
        getSwipedArea.init_x = x
        getSwipedArea.init_y = y

    elif event == cv2.EVENT_LBUTTONUP:
        cv2.destroyWindow('cropped line')
        cv2.destroyWindow('lined')

        width = x - getSwipedArea.init_x
        height = y - getSwipedArea.init_y


        line = small_receipt[getSwipedArea.init_y:height+getSwipedArea.init_y, 0:width+getSwipedArea.init_x]
        getSwipedArea.init_x = 0
        getSwipedArea.init_y = 0

        if (_debugging):
            cv2.imshow('cropped line', line)
        process_line(small_receipt, line)


#The good stuff happens here
def process_line(main_image, img):
    global _debugging

    #get colums
    image_copy = copy.copy(img)
    divide_points = divideImage(image_copy)

    #get each colum on it's own
    col_images = get_col_image(img, divide_points)

    #debugging
    if (_debugging):
        t =0
        for image in col_images:
            cv2.imshow('col-'+str(t), image)
            cv2.imwrite('col.jpg', image)
            output = os.system('tesseract '+' col.jpg'+' output')
            os.system('rm col.jpg')
            os.system('rm output.txt')

            t = t+1

    col_strings = get_col_strings(col_images)

    add_to_cost(col_strings)

    print 'cost now: ' + str(_cost)

def divideImage(img):
    global _debugging

    count = 0
    divide_points= []

    #Scan image by column and check for continuous white spaces
    for col in range(0, len(img[0]-1)):
        is_Free = True
        for row in range(0, len(img)-1):
            if(img[row][col][2] == 0):
                is_Free = False
                if (count > 15):
                    cv2.line(img, (col,0),(col, len(img)-1),(255 ,0 , 0), 1)
                    divide_points.append(col)
                cv2.circle(img, (col, row), 1, (0, 0, 255), 1)
                count = 0
                break
        if (is_Free):
            count  = count + 1

    if (_debugging):
        cv2.imshow('lined', img)

    return divide_points

def get_col_image(img, col_boundary):
    images = []
    for cb in range(1, len(col_boundary)):
        image = img[0: len(img), col_boundary[cb-1]-5:col_boundary[cb]-1]
        images.append(image)
    image = img[0: len(img), col_boundary[len(col_boundary)-1]:len(img[0])-1]
    images.append(image)
    return images

def get_col_strings(images):
    col_strings = []
    for image in images:
        cv2.imwrite('temp.jpg', image)
        output = os.system('tesseract temp.jpg temp')
        if (output == 'Empty page!!'):
            col_strings.append('')
            continue
        image_string = get_string('temp.txt')
        col_strings.append(image_string)
    os.system('rm temp.jpg')
    os.system('rm temp.txt')
    return col_strings

def get_string(filename):
    file = open(filename)
    string = ''
    for line in file.readlines():
        string  = string + line
    string = clean_string(string)
    return string

def clean_string(string):
    filtered_string = ''
    for char in string:
        if (char == '.' or char == ' ' or(char >= 'a' and char <= 'z') or
                (char >= 'A' and char <= 'Z') or (char >= '0' and char <='9')):
            filtered_string+=char
    return filtered_string

def add_to_cost(col_strings):
    global _cost
    temp = col_strings[0]
    num = int(temp[:len(temp)-1])
    total = float(col_strings[3])
    _cost = _cost + (total/num)


def main():
    global _debugging

    #Getting input right
    if (len(sys.argv) == 2):
        imageURL = sys.argv[1]
    elif (len(sys.argv ) == 3 and sys.argv[1]== '-debugging'):
        imageURL = sys.argv[2]
        _debugging = True
    else:
        print 'wrong inputs quitting...'
        return

    receipt = cv2.imread(imageURL)

    if (_debugging):
        cv2.imshow('orginial', cv2.resize(receipt,(0, 0), fx = 0.25, fy = 0.25))

    receipt = cv2.medianBlur(receipt, 9) #median filter
    _,receipt = cv2.threshold(receipt, 127, 255, cv2.THRESH_BINARY) #thresholding

    #resizing
    if len(receipt) > 1000:
        small_receipt = cv2.resize(receipt,(0, 0), fx = 0.25, fy = 0.25)
    else:
        small_receipt = receipt



    cv2.imshow('receipt', small_receipt)
    cv2.setMouseCallback('receipt', getSwipedArea, small_receipt)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()