import requests
import csv
import lxml.html as lh

def webScrape(url, filename):

    #Create a handle, page, to handle the contents of the website
    page = requests.get(url)

    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)

    #Parse data that are stored between <tr>..</tr> of HTML
    tr_elements = doc.xpath('//tr')

    #Create empty list

    i=0
    rows=[]

    for row in tr_elements:

        cells=[]

        for col in row:
            cell = col.text_content().replace('\r\n',"")
            cells.append(cell.replace('*',""))
            print("Processing: ", cell)

        rows.append(cells)

    print("Obtained Table rows: ", rows)

    #To CSV Operation
    f = open(filename, 'w')

    with f:

        writer = csv.writer(f)

        for row in rows:
            writer.writerow(row)