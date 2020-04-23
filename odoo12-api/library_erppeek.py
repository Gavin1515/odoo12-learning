#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Gavin

import erppeek
client = erppeek.Client('http://192.168.99.116:8069', 'dev12', 'admin', 'admin')
print(client)
books = client.search('library.book',[('name','ilike','odoo')])
print(books)
print(client.upgrade('library_app'))
'''
<Client 'http://192.168.99.116:8069/xmlrpc#dev12'>
[3]
1 module(s) selected
3 module(s) to process:
  to upgrade	library_app
  to upgrade	library_checkout
  to upgrade	library_member
None
'''


# C:\Users\Gavin\AppData\Roaming\Python\Python35\site-packages>python erppeek.py --server="http://192.168.99.116:8069" -d dev12 -uadmin
"""erppeek CLI Use:
Usage (some commands):
    models(name)                    # List models matching pattern
    model(name)                     # Return a Model instance
    model(name).keys()              # List field names of the model
    model(name).fields(names=None)  # Return details for the fields
    model(name).field(name)         # Return details for the field
    model(name).browse(domain)
    model(name).browse(domain, offset=0, limit=None, order=None)
                                    # Return a RecordList

    rec = model(name).get(domain)   # Get the Record matching domain
    rec.some_field                  # Return the value of this field
    rec.read(fields=None)           # Return values for the fields

    client.login(user)              # Login with another user
    client.connect(env)             # Connect to another env.
    client.modules(name)            # List modules matching pattern
    client.upgrade(module1, module2, ...)
                                    # Upgrade the modules

Password for 'admin':
Logged in as 'admin'
dev12 >>> models('book')
{'LibraryBook': <Model 'library.book'>,
 'LibraryBookCategory': <Model 'library.book.category'>}
dev12 >>> Book = model('library.book')
dev12 >>> Book.keys()
['__last_update',
 'active',
 'author_ids',
 'avg_rating',
 'book_type',
 'copies',
 'create_date',
 'create_uid',
 'currency_id',
 'date_published',
 'descr',
 'display_name',
 'id',
 'image',
 'is_available',
 'isbn',
 'last_borrow_date',
 'name',
 'notes',
 'price',
 'publisher_country_id',
 'publisher_id',
 'write_date',
 'write_uid']
dev12 >>> Model.fields(names=['name','isbn'])
{'isbn': {'change_default': False,
          'company_dependent': False,
          'depends': [],
          'help': 'Use a valid ISBN-13 or ISBN-10.',
          'manual': False,
          'readonly': False,
          'required': False,
          'searchable': True,
          'sortable': True,
          'store': True,
          'string': 'ISBN',
          'translate': False,
          'trim': True,
          'type': 'char'},
 'name': {'change_default': False,
          'company_dependent': False,
          'depends': [],
          'help': 'Book cover title',
          'manual': False,
          'readonly': False,
          'required': True,
          'searchable': True,
          'sortable': True,
          'store': True,
          'string': 'Title',
          'translate': False,
          'trim': True,
          'type': 'char'}}
dev12 >>> books = Book.browse([('name','ilike','odoo')])
dev12 >>> books
<RecordList 'library.book,[1]'>
dev12 >>> Book.get([('name','ilike','odoo')])
<Record 'library.book,1'>
"""