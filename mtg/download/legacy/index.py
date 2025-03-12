import os
import json


class Card(object):
    def __init__(self, _name, _printed_name, _set, _id, 
        _lang, _front_png_filepath, _back_png_filepath, 
        _front_img_url, _back_img_url, _type_line, 
        _doubleFace=False):

        self.name = _name
        self.printed_name = _printed_name
        self.set = _set
        self.id = _id
        self.lang = _lang
        self.front_png_filepath = _front_png_filepath
        self.back_png_filepath = _back_png_filepath
        self.front_img_url = _front_img_url
        self.back_img_url = _back_img_url
        self.type_line = _type_line
        self.doubleFace = _doubleFace

    def dumpJson(self):
        return (json.dumps(self, default=lambda obj: obj.__dict__, 
            sort_keys=True, ensure_ascii=False, indent=4))


class MTGIndex(object):

    def __init__(self, sets_dirpath, setlangs):
        self.sets_dirpath = sets_dirpath
        self.setlangs = setlangs
        # name to card_list
        self.index = dict()


    def findCardByName(self, name):
        if name in self.index:
            return self.index[name]
        else:
            return None


    def createIndex(self):
        self.index.clear()
        for _setlang in self.setlangs:
            work_dirpath = os.path.join(self.sets_dirpath, _setlang)
            info_dirpath = os.path.join(work_dirpath, "info")
            png_dirpath = os.path.join(work_dirpath, "png")

            for filename in os.listdir(info_dirpath):
                info_filepath = os.path.join(info_dirpath, filename)
                with open(info_filepath, encoding='utf-8') as fh:
                    jobj = json.load(fh)
                    _set = jobj['set']
                    _id = jobj['collector_number']
                    _lang = jobj['lang']

                    uniq_card_id = "%s_%s" % (_set, _id)
                    
                    if 'image_uris' not in jobj:
                        if 'card_faces' in jobj:
                            # two-faces card
                            _front_name = jobj['card_faces'][0]['name']
                            _front_printed_name = _front_name
                            if "printed_name" in jobj['card_faces'][0]:
                                _front_printed_name = jobj['card_faces'][0]['printed_name']
                            _front_img_url = jobj['card_faces'][0]['image_uris']['png']
                            _front_png_filename = "%s_%s.png" % (_set, _id)
                            _front_png_filepath = os.path.join(png_dirpath, _front_png_filename)
                            _front_type_line = jobj['card_faces'][0]['type_line']

                            _back_name = jobj['card_faces'][1]['name']
                            _back_printed_name = _back_name
                            if "printed_name" in jobj['card_faces'][1]:
                                _back_printed_name = jobj['card_faces'][1]['printed_name']
                            _back_img_url = jobj['card_faces'][1]['image_uris']['png']
                            _back_png_filename = "%s_%s_back.png" % (_set, _id)
                            _back_png_filepath = os.path.join(png_dirpath, _back_png_filename)
                            _back_type_line = jobj['card_faces'][1]['type_line']


                            if _front_name not in self.index:
                                self.index[_front_name] = list()
                            self.index[_front_name].append(Card(_front_name, _front_printed_name, 
                                _set, _id, _lang, _front_png_filepath, _back_png_filepath,
                                _front_img_url, _back_img_url, _front_type_line, _doubleFace=True))

                            if _back_name not in self.index:
                                self.index[_back_name] = list()
                            self.index[_back_name].append(Card(_back_name, _back_printed_name, 
                                _set, _id, _lang, _front_png_filepath, _back_png_filepath,
                                _front_img_url, _back_img_url, _back_type_line, _doubleFace=True))
                    else:
                        _name = jobj['name']
                        _printed_name = _name
                        _type_line = jobj['type_line']
                        if 'printed_name' in jobj:
                            _printed_name = jobj["printed_name"]
                        _front_img_url = jobj['image_uris']['png']
                        _front_png_filename = "%s_%s.png" % (_set, _id)
                        _front_png_filepath = os.path.join(png_dirpath, _front_png_filename)

                        if _name not in self.index:
                            self.index[_name] = list()
                        self.index[_name].append(Card(_name, _printed_name, 
                            _set, _id, _lang, _front_png_filepath, None,
                            _front_img_url, None, _type_line, _doubleFace=False))


def main():
    mtgIndex = MTGIndex(sets_dirpath='../sets', setlangs=[
        'xln/en', 'xln/zhs'])
    mtgIndex.createIndex()

    print(len(mtgIndex.index))

    rs_list = mtgIndex.findCardByName(name='Herald of Secret Streams')
    if rs_list != None:
        for el in rs_list:
            print(el.dumpJson())


if __name__ == '__main__':
    main()