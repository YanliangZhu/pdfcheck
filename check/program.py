'''
conda install -c conda-forge poppler
pip install pdf2image
pip install opencv-python
'''

import pandas as pd
import numpy as np
from pdf2image import convert_from_path
import cv2

def PDF2image(filepath):
    pages = convert_from_path(filepath, 100)
    return pages

def imageCompare(image1, image2):
    def mse(img1, img2):
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        mse = err / (float(h*w))
        return mse
    
    image1 = cv2.imread(image1)
    image2 = cv2.imread(image2)
    image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    error = mse(image1, image2)
    return error

def comparePDF(file1, file2):
    # convert PDF2image
    images1 = PDF2image(file1)
    images2 = PDF2image(file2)
    # creat df
    col = {'file1':images1, "file2":images2}
    try:
        df_image = pd.DataFrame(col)
        for i in range(len(df_image.index)):
            df_image.loc[i, 'file1'].save('image1.jpg')
            df_image.loc[i, 'file2'].save('image2.jpg')
            error = imageCompare('image1.jpg', 'image2.jpg')
            if error <= 0.00001:
                print(f'page {i+1} match: error={error}')
            else:
                print(f'issue with page {i+1}: error={error}')
        df_image.iloc[0:0] #clear df just in case
        return True
        
    except:
        #if page number differ
        df_image.iloc[0:0] #clear df just in case
        print('Page number does not match, or page size differ')
        return False

comparePDF("test1.pdf","test2.pdf")