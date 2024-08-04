import os
import time
import json
import codecs
import requests

from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType

from hts.GridImagesDrawer import GridImagesDrawer


QiJiZeiCode = 'AAEDAaIHBvuWBPqgBIahBLWhBNyhBKWjBAz8lQT9lQTclgTqlgT4oATUoQTdoQTfoQTkoQTnoQTooQSTogQA'
PaoXiaoDeCode = 'AAEDAZICBK+hBLWhBMmhBI+jBA3ZlQTblQTclQSwlgTdlgTQoQTpoQTwoQTxoQSTogS9owTKowTFqgQA'


CARD_RENDER_URL_TEMPLATE = \
    'https://art.hearthstonejson.com/v1/render/latest/%s/512x/%s.png'


def encode_decode_demo():
    # EncodingDemo
    # Create a deck from a deckstring
    deck = Deck()
    deck.heroes = [7]  # Garrosh Hellscream
    deck.format = FormatType.FT_WILD
    # Nonsense cards, but the deckstring doesn't validate.
    deck.cards = [(1, 3), (2, 3), (3, 3), (4, 3)]  # id, count pairs
    assert deck.as_deckstring == "AAEBAQcAAAQBAwIDAwMEAwA="

    # DecodingDemo 
    # Import a deck from a deckstring
    deck = Deck.from_deckstring("AAEBAQcAAAQBAwIDAwMEAw==")
    assert deck.heroes == [7]
    assert deck.format == FormatType.FT_WILD
    assert deck.cards == [(1, 3), (2, 3), (3, 3), (4, 3)]


def download_file_to_local(url, filepath):
    try:
        response = requests.get(url, stream=True)
        # 检查请求是否成功
        if response.status_code == 200:
            # 打开一个文件用于写入
            with open(filepath, 'wb') as f:
                # 将内容写入文件
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        else:
            print(f'DownloadFile({url} Failed By status_code={response.status_code})')
            return False
    except Exception as e:
        print(f'DownloadFile({url} Failed By {e})')
        return False


class DeckManager(object):
    def __init__(self, cards_json_filepath,
                 images_cache_dirpath):
        self.cards_json_filepath = cards_json_filepath
        self.images_cache_dirpath = images_cache_dirpath
        self.grid_images_drawer = GridImagesDrawer()

        self.dbfId2CardsMap = dict()

        # indexing cards by dbfId
        with codecs.open(self.cards_json_filepath, 
                         mode='r', encoding='utf-8') as fp:
            json_card_array = json.loads(fp.read())
            for json_card in json_card_array:
                self.dbfId2CardsMap[json_card['dbfId']] = json_card

    def get_card_info_by_dbfId(self, dbfId):
        if dbfId in self.dbfId2CardsMap:
            return self.dbfId2CardsMap[dbfId]
        else:
            return None
        
    def get_image_filepath_by_cardId(self, cardId):
        filepath = os.path.join(self.images_cache_dirpath,
                                '%s.png' % cardId) 

        if not os.path.exists(filepath):
            download_url = CARD_RENDER_URL_TEMPLATE % ('zhCN', cardId)
            rc = download_file_to_local(download_url, filepath)
            retryCnt = 1
            while not rc and retryCnt <= 3:
                time.sleep(1)
                rc = download_file_to_local(download_url, filepath)
                retryCnt += 1
            
            if not rc:
                return None
        
        return filepath
    
    # get if an image is already in cache,
    # if not then download it to the cache.
    def get_image_filepath_by_dbfId(self, dbfId):
        card = self.get_card_info_by_dbfId(dbfId)
        cardId = card['id']
        return self.get_image_filepath_by_cardId(cardId)
        

    def get_all_card_image_filepath_list(self, deckstring):
        deck = Deck.from_deckstring(deckstring)
        dbfIds = []
        # for _id in deck.heroes:
        #    dbfIds.append(_id)
        for _id, freq in deck.cards:
            for i in range(freq):
                dbfIds.append(_id)
        filepath_list = []
        for dbfId in dbfIds:
            filepath = self.get_image_filepath_by_dbfId(dbfId)
            assert filepath is not None
            filepath_list.append(filepath)
        return filepath_list 
    

    def conv_deckstring_list_to_grid_images(self, deckstring_list,
                                            output_keyname,
                                            output_image_dirpath,
                                            extra_card_id_list=[],
                                            isCardBack=False):
        image_filepath_list = []
        for deckstring in deckstring_list:
            image_filepath_list.extend(
                self.get_all_card_image_filepath_list(deckstring))
        for card_id in extra_card_id_list:
            filepath = self.get_image_filepath_by_cardId(card_id)
            assert filepath is not None
            image_filepath_list.append(filepath)
        
        
        self.grid_images_drawer.draw(image_filepath_list, output_keyname,
                                     output_image_dirpath, isCardBack) 

