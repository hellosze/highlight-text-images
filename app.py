#inspired by https://stackoverflow.com/questions/54115780/highlighting-specific-text-in-an-image-using-python
# this script highlights text where the word is optimera and input file is an image, preferrably a screenshot
import cv2,re
import pytesseract
import streamlit as st

uploaded_files = st.file_uploader(
    "Choose an image file", accept_multiple_files=True
)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    # st.write(bytes_data)
    
    filename = uploaded_file.name
    # filename = 'nationalpost_gam.png'
    # text_search = "optimera"
    text_search = "optimera=Z,"
    # text_search = "optimera=Z(,[A-Z]\d+){8}"
    # text_search = "optimera=Z(,[A-Z][A-Z]?\d+)*"
    # text_search = r"ad\-[A-Z][0-9]{6}"
    # text_search = r"ad-\w{6}"
    # text_search = "arn-viafoura"
    # read the image
    img = cv2.imread(filename)
    
    # run tesseract, returning the bounding boxes
    data = pytesseract.image_to_data(img, output_type='dict')
    print(data)
    boxes = len(data['level'])
    
    for i in range(boxes):
        if re.search(text_search , data['text'][i], re.MULTILINE):
            print("Found text")
            overlay = img.copy()
            (x, y, w, h) = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
    
            print(x, y, w, h)
            cv2.rectangle(overlay, (data['left'][i], data['top'][i]), (data['left'][i]+data['width'][i], data['top'][i]+data['height'][i]),(255,255,0), -1)
            alpha = 0.2  # Transparency factor.
            # Following line overlays transparent rectangle over the image
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
    cv2.imwrite("output.jpg",img)
    
    st.image("output.jpg")
