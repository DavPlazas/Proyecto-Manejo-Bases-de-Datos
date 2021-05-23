# -*- coding: utf-8 -*-
"""
Created on Sat May 22 21:40:57 2021

@author: David
"""

import psycopg2

class Connection:
    
    def __init__(self):
        self.connection = None
    
    def openConnection(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                               password="Veneno2003",
                                               database="proyecto",
                                               host="localhost", 
                                               port="5432")
        except Exception as e:
            print (e)

    def closeConnection(self):
        self.connection.close()