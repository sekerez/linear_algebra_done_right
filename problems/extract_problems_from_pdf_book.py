#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright: 2022 Shivam Sharma <shivam.src@gmail.com>
# License: GNU GPL v2 or higher
# This is a demonstration of how to scrape the problems from a Mathematics textbook PDF. It requires a PDF parsing library and MathPix API (which is paid). Free alternatives to MathPix are available too however they are cumbersome to use.
# NOTE:
# 1. This script was designed for Linear Algebra Done Right, 3rd Edition. I had cropped the LADR PDF to remove the header and footer from each page (which contained the page number and section title). This made parsing much easier. Note that your cropping software may often not "truly" crop the PDF, so it's best to "print" the PDF (as another PDF) after cropping it. This printed PDF will now be "truly" cropped.
# 2. MathPix API returns the markdown in its own Mathpix-flavoured Markdown, which is a superset of markdown. This makes some of the latex equations not render correctly on Github. TODO: Find a way to convert this markdown to Github-flavoured Markdown.
# 3. I've used 2 PDF parsing libs. One excelled at parsing while the other excelled at cropping it and converting it into images. TODO: Maybe I can do it with just one.

import requests, json, re, os
from pathlib import Path
from py_pdf_parser.loaders import load_file
import pdfplumber
from wand.image import Image
from time import sleep

#For MathPix API, you need to pay 20$ one-time fee and then use it for free forever (for <1000 requests per month)
MATHPIX_APP_ID = os.environ.get("MATHPIX_APP_ID")
MATHPIX_APP_KEY = os.environ.get("MATHPIX_APP_KEY")
if not MATHPIX_APP_ID or not MATHPIX_APP_KEY:
    print("You gotta set the mathpix api id and keys in your environment bro! I won't proceed without them.")
    raise SystemExit(101)

file = "LADR_.pdf"
print(f"""Script usage: keep the cropped PDF in the same folder as this script with filename : {file}. 
      This script will scrape the PDF and extract all the exercises problems as image files.
      These image files are then sent to MathPix API to get the exercise problems as markdown.
      MathPix API requires 20$ one-time fee and then limited free usage forever""")
if not input("All set? Shall we proceed? (y/n)") == 'y':
    print("Exiting early.")
    raise SystemExit(101)

RESOLUTION = 100 #For images

def find():
    '''
    finds the exercise sections, returning the starting and end elements for it
    the end elements are the starting of the next section (or chapter)
    '''
    start = None
    for i, e in enumerate(document.elements):
        if (re.search(r'exercises\s\d+$', e.text().lower()) \
                or re.search(r'exercises\s\d+\.[a-z]$', e.text().lower())) \
                and e.page_number > 26:
            #  start = (i, e.text(), e.page_number, e.bounding_box)
            start = i
        if start and e.font_size > 15: #normal text font size is 10.9. Headings usually start with size 17.2
                #  end = (i, e.text(), e.page_number, e.bounding_box)
                end = i
                yield start, end
                start = None


def mathpix(imgFile):
    r = requests.post("https://api.mathpix.com/v3/text",
        files={"file": open(imgFile,"rb")},
        data={
          "options_json": json.dumps({
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True
          })
        },
        headers={
            "app_id": MATHPIX_APP_ID,
            "app_key": MATHPIX_APP_KEY
        }
    )
    if r.status_code == 200:
        return r.json()['text']
    else:
        return None


if __name__ == '__main__':

    document = load_file(file)
    pdf = pdfplumber.open(file)
    Path("images").mkdir(parents=True, exist_ok=True) #for saving the images as one consolated image for each exercise section
    Path("markdown").mkdir(parents=True, exist_ok=True) #for saving the images converted to latex equations (one latex or markdown file per question)

    print(f"Alright, going for the kill, brothers. See you in Valhalla!")
    for start, end in find():
        startPage = document.elements[start].page_number
        endPage = document.elements[end].page_number

        title = document.elements[start].text() #the exercise section title

        e = document.elements[start+1] #we skip the very first element (which is the exercise title)
        bb = e.bounding_box
        page = pdf.pages[startPage-1]
        page.crop(bbox=(0,page.height - bb.y1,page.width,page.height)).to_image(resolution=RESOLUTION).save('page0.png')

        for i,n in enumerate(range(startPage+1, endPage)):
            page = pdf.pages[n-1].to_image(resolution=RESOLUTION).save(f'page{i+1}.png')

        #Removing overt whitespace border from each image
        for i,n in enumerate(range(startPage, endPage)):
            with Image(filename=f'page{i}.png') as output:
                output.trim()
                output.border(color='#fff', width=20, height=20)
                output.save(filename=f'page{i}.png')

        #Querying mathpix and converting to latex
        latex = ''
        for i,n in enumerate(range(startPage, endPage)):
            if text := mathpix(f'page{i}.png'):
                print(f"Mathpix succceeded for page{i}.png")
                latex = latex + "\n" + text
            else:
                latex = None #We won't be processing this exercise at all and try again later (लैटर औन) on.
                print(f"Skipping the exercise: {title}")
                break
        if latex:
            exercise = title.split()[1]
            questions = re.findall(r'(?ms)^\d+\s[A-Z(].+?(?=^\d+\s[A-Z(]|\Z)', latex)
            for i, q in enumerate(questions):
                with open(f'markdown/{exercise}.{i+1}.md', 'w') as f:
                    f.write(q)

        #  import ipdb; ipdb.set_trace()

        #Joining all the images vertically (stacked)
        with Image(filename='page0.png') as output:
            for i,n in enumerate(range(startPage+1, endPage)):
                output.sequence.append(image=Image(filename=f'page{i+1}.png'))
            output.smush(stacked=True)
            output.save(filename=f'images/{title}.png')

        #Cleanup
        for i,n in enumerate(range(startPage, endPage)):
            os.remove(f'page{i}.png')

        sleep(0.4) #So that Mathpix API is not overwhelmed
