#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

from argparse import ArgumentParser
from library_odoorpc import LibraryAPI

parser = ArgumentParser()
parser.add_argument('command', choices=['list','add','set-title','del'])
parser.add_argument('params', nargs='*') # 可选参数
args = parser.parse_args() # Namespace(command='list', params=['New'])
print(args)

srv, port, db, user, pwd = '192.168.99.116', 8069, 'dev12', 'admin', 'admin'
api = LibraryAPI(srv, port, db, user, pwd)

if args.command == 'list':
    text = args.params[0] if args.params else None
    books = api.search_read(text)
    for book in books:
        print('%(id)d %(name)s' % book)
if args.command == 'add':
    for title in args.params:
        new_id = api.create(title)
        print('Book added with ID %d.' % new_id)
if args.command == 'set-title':
    if len(args.params) != 2:
        print('Set command requires a title and ID.')
    else:
        book_id, title = int(args.params[0]), args.params[1]
        api.write(title, book_id)
        print('Title set for book ID %s.' % book_id)
if args.command == 'del':
    for param in args.params:
        api.unlink(int(param))
        print('Book with ID %s deleted.' % param)

'''python命令行测试结果：
    D:\Code\odoo12\odoo12\odoo12-learning>python library.py list
    Namespace(command='list', params=[])
    3 Brave New World
    1 Odoo12 Development Essentials
    
    D:\Code\odoo12\odoo12\odoo12-learning>python library.py list "new"
    Namespace(command='list', params=['new'])
    3 Brave New World
    
    D:\Code\odoo12\odoo12\odoo12-learning>python library.py list "new" "odoo" # 只能使用第一个参数查询
    Namespace(command='list', params=['new', 'odoo'])
    3 Brave New World
    
    D:\Code\odoo12\odoo12\odoo12-learning>python library.py add "TestBook1" "TestBook2"
    Namespace(command='add', params=['TestBook1', 'TestBook2'])
    Book added with ID 7.
    Book added with ID 8.
    
    D:\Code\odoo12\odoo12\odoo12-learning>python library.py set-title 7 "Book1"
    Namespace(command='set-title', params=['7', 'Book1'])
    Title set for book ID 7.
    
    D:\Code\odoo12\odoo12\odoo12-learning>python library.py del 7 8
    Namespace(command='del', params=['7', '8'])
    Book with ID 7 deleted.
    Book with ID 8 deleted.
'''
