import requests

README_FILE = '../README.md'

def getFile(my_file):
    f = open(my_file, 'r')
    file_lines = f.readlines()
    data = {'Producto': ['Ultima actualizacion '], '------ ': ['------ ']}
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

    return data

def write_data(my_data):
    output = ['##Esta tabla tiene el ultimo timestamp de cada producto']
    for each_prod in my_data:
        line = '|' + each_prod + '|'
        if 'producto 43' in line:
            for i in range(len(my_data[each_prod])):
                if i == 0:
                    line += my_data[each_prod][i] + '|\n'
                elif i == len(my_data[each_prod]) - 1:
                    line += '| |' + my_data[each_prod][i] + '|'
                else:
                    line += '| |' + my_data[each_prod][i] + '|\n'
        else:
            for each_time in my_data[each_prod]:
                line += each_time + '|'
        output.append(line)

    return output

def list2file(my_output, file):
    f = open(file, 'w')
    for ele in my_output:
        f.write(ele + '\n')
    f.close()

if __name__ =='__main__':
    my_data = getFile(README_FILE)
    output = write_data(my_data)
    list2file(output, '../Products_last_update.md')