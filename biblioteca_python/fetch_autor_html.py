import urllib.request
url='http://127.0.0.1:5000/Autor/'
html = urllib.request.urlopen(url).read().decode('utf-8')
with open('c:/temp/autor_html.txt','w',encoding='utf-8') as f:
    f.write(html)
print(html[:1200])
