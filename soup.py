from bs4 import BeautifulSoup
import csv, time, random
import pip._vendor.requests as request

starter = 0
def findInfo(url):
    result = []
    response = request.get(url)
    doc = BeautifulSoup(response.text, "html.parser")
    title = doc.find_all("strong")
    try:
        result.append(title[1].text.encode("utf-8"))
    except(IndexError):
        print(doc)
    list = doc.find_all("span", {"class":"dark_text"})
    for i in list:
        if(i.text == "Aired:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            result.append(string[1].encode("utf-8"))
        if(i.text == "Studios:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            result.append(string[1].encode("utf-8"))
        if(i.text == "Score:"):
            arr = i.parent.text.split(':')
            string1 = arr[1].split('\n')
            string = string1[1].split(' ')
            result.append(string[0])
        if(i.text == "Type:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            result.append(string[1].encode("utf-8"))
        if(i.text == "Source:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            result.append(string[1].encode('utf-8'))
        if(i.text == "Episodes:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            result.append(string[1])
        if(i.text == "Genres:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            for x in range(len(string)-1):
                string[x] = string[x].encode("utf-8")
            result.append(string)
        if(i.text == "Genre:"):
            arr = i.parent.text.split(':')
            string = arr[1].split('\n')
            result.append(string[1].encode("utf-8"))
    result.append(doc.find("p", {"itemprop":"description"}).text.encode("utf-8"))
    
    if len(result)<9:
        d = result[-1]
        result[-1] = "N/A"
        result.append(d)
    return result

with open("log.csv", 'w', newline='') as f:
    names = ['Title', 'Type', 'Episodes', 'Aired', 'Studio', 'Source', 'Genres', 'Score', 'Summary']
    writer = csv.DictWriter(f, fieldnames=names)
    writer.writeheader()  
    while(starter < 20700):
        url = "https://myanimelist.net/topanime.php?type=bypopularity&limit="+str(starter)
        if starter%300 == 0 and starter!=0:
            print("Waiting for bot screen...")
            time.sleep(60)
        if starter%150==0:
            time.sleep(random.randrange(10, 40))
        response = request.get(url)
        doc = BeautifulSoup(response.text, "html.parser")
        
        rows = doc.find_all("tr", {"class": "ranking-list"})
        row_num = 0
        for n in rows:
            head = n.find("h3", {"class":"hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"})
            title = head.find("a")
            
            new_url = str(title['href'])
            results = findInfo(new_url)
            

            writer.writerow({'Title':results[0], 'Type':results[1], 'Episodes':results[2], 'Aired':results[3], 'Studio':results[4], 'Source':results[5], 'Genres':results[6], 'Score':results[7], 'Summary':results[8]})
            print("row " + str(row_num) + " done!")
            row_num+=1

        starter+=50
f.close()