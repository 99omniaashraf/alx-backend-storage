#!/usr/bin/env python3
"""
mod doc
"""


def schools_by_topic(mongo_collection, topic):
    """
    func doc
    """
    return list(mongo_collection.find({"topics": topic}))
