# -*- coding: utf-8 -*-

from app import app
from model import *
import os
import shutil
import time

if os.path.exists("baseRotonde.db"):
    os.remove("baseRotonde.db")

folder = 'static/uploads'
sauvegarde = 'sauvegarde'

if os.path.exists(folder):
    shutil.rmtree(folder)
time.sleep(1)
folders = os.listdir(sauvegarde)

for fol in folders:
    if os.path.isdir(sauvegarde+'/'+fol):
        print('dir',fol)
        shutil.copytree(sauvegarde+'/'+fol, folder+'/'+fol)
    if os.path.isfile(sauvegarde+'/'+fol) and fol=="baseRotonde.db":
        shutil.copyfile(sauvegarde+'/'+fol,'./'+fol)
