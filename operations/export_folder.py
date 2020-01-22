#!/usr/bin/python3

import os
import pickle

from client.jobs_client import JobsClient

server_and_port = os.environ.get('SERVER_AND_PORT')


def load_files_list(folder_path):
    files_list_file_path = os.path.join(folder_path, "files_list.txt")
    try:
        files_list = pickle.load(open(files_list_file_path, 'rb'))
    except:
        files_list = []
    
    return files_list

def save_files_list(folder_path, files_list):
    files_list_file_path = os.path.join(folder_path, "files_list.txt")
    pickle.dump(files_list, open(files_list_file_path, 'wb'))

def import_from_folder():
    folder_path = os.environ.get('WORKING_FOLDER')

    client = JobsClient(server_and_port)

    names = [name for name in os.listdir(folder_path) if
             os.path.isfile(os.path.join(folder_path, name)) and name.endswith('.jl')]
    
    files_added = load_files_list(folder_path)
    for name in names:
        if name in files_added:
            print("file [%s] already added; continue-ing" % (name))
            continue
            
        file_path_full = os.path.join(folder_path, name)
        file_size = os.path.getsize(file_path_full)
        if file_size > 0:
            print("adding file [%s] with size %2.2f KB" % (file_path_full, file_size/1024.0))
            response = client.add_jobs_from_file(file_path_full)
            if response.status_code != 200:
                raise Exception("status_code is %d" % (response.status_code))
            
            files_added.append(name)
            save_files_list(folder_path, files_added)

def import_single_file():
    # server_and_port = 'test-jobs-api-123123.herokuapp.com:80'
    client = JobsClient(server_and_port)

    file_path_full = r'C:\postman\jobs_greenhouse_26_jobs.jl'
    file_size = os.path.getsize(file_path_full)
    if file_size > 0:
        print("adding file [%s] with size %2.2f KB" % (file_path_full, file_size / 1024.0))
        client.add_jobs_from_file(file_path_full)

def import_single_file_postman_code():
    import requests
    
    url = "http://test-jobs-api-123123.herokuapp.com:80/v1/jobs_batch"
    
    payload = {}
    # files = [('file', open('C:\postman\jobs_greenhouse_26_jobs.jl', 'rb'))]
    files = [('file', open(r'C:\postman\greenhouse_results_https___boards.greenhouse.io_accuweather___epoch1577549220__.jl', 'rb'))]
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    
    print(response.text.encode('utf8'))


def do_main():
    pass
    # import_single_file()
    # import_single_file_postman_code()
    import_from_folder()

if __name__ == '__main__':
    do_main()
