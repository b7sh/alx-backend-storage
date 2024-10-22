#!/usr/bin/env python3
'Write a Python function that lists all documents in a collection'
def list_all(mongo_collection):
    'Return an empty list if no document in the collection'
    document = mongo_collection.find()
    if document.count() == 0:
        return []
    return document
