import os
from urllib.parse import urlparse

def check_dir(directory):
    return os.path.exists(directory)


def check_project_dir():
    if not check_dir('storage'):
        os.mkdir('storage', 0o777)


def create_data_file(project_name,base_url):
    check_project_dir()
    if not check_dir('storage/' + project_name):
        os.mkdir('storage/' + project_name, 0o777)
    if not os.path.exists('storage/' + project_name + '/queue.txt'):
        file = open('storage/' + project_name + '/queue.txt', 'w')
        file.write(base_url+"\n")
    else:
        file = open('storage/' + project_name + '/queue.txt', 'wt')
        file.write(base_url + "\n")
    if not os.path.exists('storage/' + project_name + '/crawler.txt'):
        file = open('storage/' + project_name + '/crawler.txt', 'w')
    else:
        file = open('storage/' + project_name + '/crawler.txt', 'r')
    file.close()


def merge_to_file(file_name):
    data = set()
    with open(file_name, 'rt') as file:
        for line in file:
            data.add(line.replace('\n', ''))
    return data


def update_file(data, file):
    with open(file, 'w') as f:
        for line in sorted(data):
            f.write(line + '\n')

def get_domain(url):
    try:
        results = get_sub_domain(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

def get_sub_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return ''