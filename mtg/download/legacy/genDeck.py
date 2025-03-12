import os
import codecs

from index import MTGIndex
from nine_grid_pinjie import process_nine_grid_pinjie


def parse_deck_file(filepath, mtgtop8=False):
    card_list = list()
    with codecs.open(filepath, mode='r', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.rstrip("\r\n")
            if len(line) <= 0 or line.startswith("//"):
                continue

            if mtgtop8:
                line = line.replace('(', '### ')
                line = line.replace(')', '')
                line = line + ' en'

            first_space_pos = line.find(' ')
            segment_pos = line.find(' ### ')
            _size = int(line[ : first_space_pos])
            _name = line[first_space_pos+1 : ]
            if segment_pos > 0:
                _name = line[first_space_pos+1 : segment_pos]
                attrs = line[segment_pos+5:].split(" ")
                _set, _id, _lang = attrs[0], attrs[1], attrs[2]
                card_list.append({
                    "name": _name,
                    "size": _size,
                    "set": _set.lower(),
                    "id": _id,
                    "lang": _lang.lower()
                })
            else:
                card_list.append({
                    "name": _name,
                    "size": _size
                })
    return card_list


def save_cards_list_as_standard(cards_list, save_deck_filepath):
    with codecs.open(save_deck_filepath, mode='w', encoding='utf-8') as fp:
        for item in cards_list:
            card, size = item[0], item[1]
            fp.write("%d %s ### %s %s %s %s\n" % (size, card.name, 
                card.set, card.id, card.lang, card.printed_name))


def search_cards_by_deck_file(mtgIndex, deck_filepath, 
    prelangs=['zhs', 'zht', 'en'], mtgtop8=False):

    card_list = parse_deck_file(deck_filepath, mtgtop8)
    rs_list = list()
    for card in card_list:
        rs = mtgIndex.findCardByName(card['name'])
        if rs is not None and len(rs) > 0:
            found = False
            if 'set' in card and 'id' in card and 'lang' in card:
                for el in rs:
                    if el.lang == card['lang'] and \
                        el.set == card['set'] and el.id == card['id']:
                        
                        rs_list.append((el, card['size']))
                        found = True
                        break
            
            for lang in prelangs:
                if found:
                    break
                for el in rs:
                    if el.lang == lang:
                        rs_list.append((el, card['size']))
                        found = True
                        break
                
        else:
            print("Can't find %s" % card['name'])
            return list()
    return rs_list


def generate_nine_pinjie_png(cards_list, deck_name, 
    output_image_dirpath, removeBasicLand=True):

    image_filepathes = list()
    for item in cards_list:
        card, size = item[0], item[1]
        if removeBasicLand:
            if card.type_line.startswith("Basic Land — "):
                continue
        for i in range(size):
            image_filepathes.append(card.front_png_filepath)
            if card.doubleFace:
                image_filepathes.append(card.back_png_filepath)

    process_nine_grid_pinjie(image_filepathes, output_image_dirpath, 
        deck_name, saveAsJpg=True)


def batch_convert_mtgtop8_to_standard(mtgIndex, deck_dirpath, 
    converted_deck_dirpath):
    
    for deck_filename in os.listdir(deck_dirpath):
        deck_filepath = os.path.join(deck_dirpath, deck_filename)

        cards_list = search_cards_by_deck_file(mtgIndex, deck_filepath, 
            prelangs=['zhs', 'zht', 'en'], mtgtop8=True)

        save_cards_list_as_standard(cards_list, 
            save_deck_filepath=os.path.join(
                converted_deck_dirpath, deck_filename))


def batch_convert_deckfile_to_standard(mtgIndex, deck_dirpath, 
    converted_deck_dirpath):
    
    for deck_filename in os.listdir(deck_dirpath):
        deck_filepath = os.path.join(deck_dirpath, deck_filename)

        cards_list = search_cards_by_deck_file(mtgIndex, deck_filepath, 
            prelangs=['zhs', 'zht', 'en'], mtgtop8=False)

        save_cards_list_as_standard(cards_list, 
            save_deck_filepath=os.path.join(
                converted_deck_dirpath, deck_filename))


def batch_generate_nine_pinjie_png(mtgIndex, deck_dirpath, 
    output_dirpath):

    for deck_filename in os.listdir(deck_dirpath):
        deck_filepath = os.path.join(deck_dirpath, deck_filename)

        cards_list = search_cards_by_deck_file(mtgIndex, deck_filepath, 
            prelangs=['zhs', 'zht', 'en'])

        generate_nine_pinjie_png(cards_list, deck_name=deck_filename, 
            output_image_dirpath='../decks/output')


def main():
    mtgIndex = MTGIndex(sets_dirpath='../sets', setlangs=[
        'xln/en', 'xln/zhs', 'rix/en', 'rix/zhs'])
    mtgIndex.createIndex()

    # batch_convert_deckfile_to_standard(mtgIndex, deck_dirpath='../decks/precon_decks/rix', 
    #     converted_deck_dirpath)

    batch_convert_mtgtop8_to_standard(mtgIndex, deck_dirpath='../decks/mtgtop8/standard', 
        converted_deck_dirpath)

    # batch_generate_nine_pinjie_png(mtgIndex, converted_deck_dirpath='../decks/tobe_gen', 
    #     output_dirpath='../decks/output')


if __name__ == "__main__":
    main()

