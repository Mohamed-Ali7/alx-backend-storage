#!/usr/bin/env python3
"""This module contains insert_school() function"""

def insert_school(mongo_collection, **kwargs):
    """Inserts a new document in a collection based on kwargs:"""

    new_school = mongo_collection.insert_one(kwargs)
    return new_school.inserted_id
