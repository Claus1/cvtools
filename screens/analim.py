from cv import *
from unigui import *
from common import *
from config import *

name = "Image analysis"
icon = 'image_search'
order = 3

table4image = Table('Image classification', None, headers = ['Group', 'Probability'], tools = False, rows = [])

def dialog_callback(_, bname):
    if bname == 'Ok':
        user.progress('Creating index..')
        create_index()
        switch_search.value = True
    else:
        switch_search.value = False
    return switch_search

def build_index(_, v):
    if v and not exists(fvector_index):
        return Dialog('Image index does not exist. Create it?', dialog_callback)
    _.value = v

switch_search = Switch('Search', exists(fvector_index), build_index, icon= 'tips_and_updates')
how_many = Edit('How many images to search', 20, type = 'number')

similar_block = Block('Similar images', [switch_search, how_many], icon='view_module', scroll=True, scaler=True)

def analyze_image(_, path):
    table4image.rows = classify_image(path)
    if switch_search.value:
        idata = search_image(path, how_many.value)
        images = [Image(imd[0], False, header=f'{imd[1]} {[imd[2]]}', width= 300, height= 200) for imd in idata]
        similar_block.value = [similar_block.value[0], images]
    return table4image, similar_block

block_image = Block('Image Analysis', UploadImageButton('Load an image', analyze_image), table4image, 
                    icon = 'youtube_searched_for')

blocks= [block_image, similar_block]