import bs4, requests, os, csv
import time, json

def main():

    #Init
    base_path = os.path.dirname(__file__)
    config = json.load(open(os.path.join(base_path, 'config.json')))
    fn = config['DataSet']['NPMCorpus']

    for i in range(config['DataSet']['Quantity']):

        dataStartnum = config['NPM']['ID']
        dataURLnum = "0"+ str(int(dataStartnum)+i)
        print(dataURLnum)

        url = config['DataSet']['URL'] + dataURLnum 
        
        time.sleep(2.5)
        
        try:
            html = requests.get(url)
        except:
            time.sleep(10)
            continue

        print("Page Downloading...")
        
        if(html.status_code == requests.codes.ok):

            print("Page Download Sucessful")

            objSoup = bs4.BeautifulSoup(html.text, 'lxml')

            dataTag=objSoup.select('.project-detail')

            artworksName_box = dataTag[0].find('h3')
            artworksName=artworksName_box.text
            print(artworksName)

            rows = dataTag[0].find_all('li')
            getContent=rows[-1].text
            if (getContent[0]=="說"):
                artworksContent_box=getContent
                artworksContent=artworksContent_box[4:]

                with open(fn, 'a', newline='',encoding = 'utf-8-sig') as csvFile:
                    csvWriter=csv.writer(csvFile)
                    csvWriter.writerow([artworksName,artworksContent,url])

                print(artworksContent)
        else:
            print("Page Download failed")

if __name__ == '__main__':
    main()