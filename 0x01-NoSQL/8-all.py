#!/usr/bin/env python3
"""This module contains list_all() function"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection or
    Return an empty list if no document in the collection
    """
    return mongo_collection.find()
