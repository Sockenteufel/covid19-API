import requests

README_FILE = '../README.md'

def getFile(my_file):
    f = open(my_file, 'r')
    file_lines = f.readlines()
    data = {'| Producto |': '| Ultima actualizacion |', '|------| ': '|------| '}
    last_updates = []
    prod = ''
    for each_line in file_lines:
        if '[Ultimo registro]' in each_line:
            api = each_line.replace('[Ultimo registro]', '').replace('(http', 'http').replace('%22)', '%22')
            #print(api)
            r = requests.get(api)
            #print(r.json()['results'][0]['series'][0]['values'][0][0])
            last_updates.append(r.json()['results'][0]['series'][0]['values'][0][0])
        elif '* [producto' in each_line or '* producto' in each_line:
            last_updates = []
            beginning = each_line.find('producto')
            if ']' in each_line:
                end = each_line.find(']')
            elif ':' in each_line:
                end = each_line.find(':')
            prod = each_line[beginning:end]
        if len(prod) > 1:
            data[prod] = last_updates

    print(data)


if __name__ =='__main__':
    getFile(README_FILE)