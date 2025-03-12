import os
import json
import requests
import PIL.Image as Image
import urllib.parse


from downloadSets import download2File, downloadCheckList


SET_DIRPATH = '../current'
# SET_DIRPATH = '../sets'


def check_image_file(img_url, png_dirpath, output_filename):
    saved_png_filepath = os.path.join(png_dirpath, output_filename)
    try:
        im = Image.open(saved_png_filepath)
    except:
        print({"type": "image", "url": img_url, "filepath": saved_png_filepath})
        download2File(img_url, png_dirpath, output_filename)


def fix_info_file(card, setId, lang='en',):
    set_dirpath = os.path.join(SET_DIRPATH, setId)
    work_dirpath = os.path.join(set_dirpath, lang)
    uniq_card_id = card['card_id'].replace("/", "_")
    if lang != 'en':
        uniq_card_id = uniq_card_id[:uniq_card_id.rfind("_")]
    card_id = card['card_id']
    info_url_template = "https://api.scryfall.com/cards/%s?format=json&pretty=true"
    info_url = info_url_template % card_id

    print({"type": "info", "url": info_url,
        "filepath": os.path.join('%s/%s/info' % (setId, lang), '%s.json' % uniq_card_id)})

    download2File(info_url, '%s/%s/%s/info' % (SET_DIRPATH, setId, lang),
        '%s.json' % uniq_card_id)


def check_set(setId, lang='en'):
    set_dirpath = os.path.join(SET_DIRPATH, setId)
    work_dirpath = os.path.join(set_dirpath, lang)

    print('checking for set %s/%s with work_dirpath = %s' % (setId, lang, work_dirpath))
    card_check_list = downloadCheckList(setId, lang)

    for card in card_check_list:
        # 1. info is ok?
        uniq_card_id = card['card_id'].replace("/", "_")
        if lang != 'en':
            uniq_card_id = uniq_card_id[:uniq_card_id.rfind("_")]
        info_filepath = os.path.join(work_dirpath, 'info/%s.json' % uniq_card_id)

        try:
            with open(info_filepath, encoding='utf-8') as fh:
                jobj = json.load(fh)
                collection_set = jobj['set']
                collector_number = jobj['collector_number']
                target_id = urllib.parse.quote("%s_%s" % (collection_set, collector_number))
                # print(uniq_card_id)
                # print(target_id)
                if uniq_card_id.startswith(target_id):
                    # info file is ok
                    png_dirpath = os.path.join(work_dirpath, "png")
                    if 'image_uris' not in jobj:
                        if 'card_faces' in jobj:
                            # two-faces card
                            img_url_front = jobj['card_faces'][0]['image_uris']['png']
                            output_filename = "%s_%s.png" % (collection_set, collector_number)
                            check_image_file(img_url_front, png_dirpath, output_filename)

                            img_url_back = jobj['card_faces'][1]['image_uris']['png']
                            output_filename = "%s_%s_back.png" % (collection_set, collector_number)
                            check_image_file(img_url_back, png_dirpath, output_filename)
                    else:
                        img_url = jobj['image_uris']['png']
                        output_filename = "%s_%s.png" % (collection_set, collector_number)
                        check_image_file(img_url, png_dirpath, output_filename)
                else:
                    # info file is wrong
                    fix_info_file(card, setId, lang)
        except Exception as e:
            fix_info_file(card, setId, lang)

    print('checking done!')


checkedSets = [
{
    "SetName": "Ixalan",
    "SetId": "xln",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Ixalan Promos",
    "SetId": "pxln",
    "Lang": ['en']
},
{
    "SetName": "Ixalan Tokens",
    "SetId": "txln",
    "Lang": ['en']
},
{
    "SetName": "XLN Treasure Chest",
    "SetId": "pxtc",
    "Lang": ['en']
},
{
    "SetName": "XLN Standard Showdown",
    "SetId": "pss2",
    "Lang": ['en']
},
{
    "SetName": "Rivals of Ixalan",
    "SetId": "rix",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Rivals of Ixalan Promos",
    "SetId": "prix",
    "Lang": ['en']
},
{
    "SetName": "Rivals of Ixalan Tokens",
    "SetId": "trix",
    "Lang": ['en']
},
{
    "SetName": "Dominaria",
    "SetId": "dom",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Dominaria Promos",
    "SetId": "pdom",
    "Lang": ['en']
},
{
    "SetName": "Dominaria Tokens",
    "SetId": "tdom",
    "Lang": ['en']
},
{
    "SetName": "Core Set 2019",
    "SetId": "m19",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Core Set 2019 Promos",
    "SetId": "pm19",
    "Lang": ['en']
},
{
    "SetName": "Core Set 2019 Tokens",
    "SetId": "tm19",
    "Lang": ['en']
},
{
    "SetName": "M19 Gift Pack",
    "SetId": "g18",
    "Lang": ['en']
},
{
    "SetName": "M19 Standard Showdown",
    "SetId": "pss3",
    "Lang": ['en']
},
{
    "SetName": "Guilds of Ravnica",
    "SetId": "grn",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Guilds of Ravnica Promos",
    "SetId": "pgrn",
    "Lang": ['en']
},
{
    "SetName": "Guilds of Ravnica Tokens",
    "SetId": "tgrn",
    "Lang": ['en']
},
{
    "SetName": "GRN Ravnica Weekend",
    "SetId": "prwk",
    "Lang": ['en']
},
{
    "SetName": "Ravnica Allegiance",
    "SetId": "rna",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Ravnica Allegiance Promos",
    "SetId": "prna",
    "Lang": ['en']
},
{
    "SetName": "Ravnica Allegiance Tokens",
    "SetId": "trna",
    "Lang": ['en']
},
{
    "SetName": "RNA Ravnica Weekend",
    "SetId": "prw2",
    "Lang": ['en']
},
{
    "SetName": "War of the Spark",
    "SetId": "war",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "War of the Spark Promos",
    "SetId": "pwar",
    "Lang": ['en']
},
{
    "SetName": "War of the Spark Tokens",
    "SetId": "twar",
    "Lang": ['en']
},
{
    "SetName": "Modern Horizons",
    "SetId": "mh1",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Modern Horizons Promos",
    "SetId": "pmh1",
    "Lang": ['en']
},
{
    "SetName": "Modern Horizons Tokens",
    "SetId": "tmh1",
    "Lang": ['en']
},
{
    "SetName": "Modern Horizons Art Series",
    "SetId": "amh1",
    "Lang": ['en']
},
{
    "SetName": "Core Set 2020",
    "SetId": "m20",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Core Set 2020 Promos",
    "SetId": "pm20",
    "Lang": ['en']
},
{
    "SetName": "Core Set 2020 Tokens",
    "SetId": "tm20",
    "Lang": ['en']
},
{
    "SetName": "M20 Promo Packs",
    "SetId": "ppp1",
    "Lang": ['en']
},
{
    "SetName": "Throne of Eldraine",
    "SetId": "eld",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Throne of Eldraine Promos",
    "SetId": "peld",
    "Lang": ['en']
},
{
    "SetName": "Throne of Eldraine Tokens",
    "SetId": "teld",
    "Lang": ['en']
},
{
    "SetName": "Theros Beyond Death",
    "SetId": "thb",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Theros Beyond Death Promos",
    "SetId": "pthb",
    "Lang": ['en']
},
{
    "SetName": "Theros Beyond Death Tokens",
    "SetId": "tthb",
    "Lang": ['en']
},
{
    "SetName": "Ikoria: Lair of Behemoths",
    "SetId": "iko",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{
    "SetName": "Ikoria: Lair of Behemoths Promos",
    "SetId": "piko",
    "Lang": ['en']
},
{
    "SetName": "Ikoria: Lair of Behemoths Tokens",
    "SetId": "tiko",
    "Lang": ['en']
},
{ 
    "SetName": "Core Set 2021",
    "SetId": "m21",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Core Set 2021 Promos",
    "SetId": "pm21",
    "Lang": ['en']
},
{ 
    "SetName": "Core Set 2021 Tokens",
    "SetId": "tm21",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising",
    "SetId": "znr",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Zendikar Rising Expeditions",
    "SetId": "zne",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising Promos",
    "SetId": "pznr",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising Tokens",
    "SetId": "tznr",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising Minigames",
    "SetId": "mznr",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising Art Series",
    "SetId": "aznr",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising Commander",
    "SetId": "znc",
    "Lang": ['en', 'zhs', 'ja']
},
{ 
    "SetName": "Zendikar Rising Commander Tokens",
    "SetId": "tznc",
    "Lang": ['en']
},
{ 
    "SetName": "Zendikar Rising Substitute Cards",
    "SetId": "sznr",
    "Lang": ['en']
},
{ 
    "SetName": "Commander Legends",
    "SetId": "cmr",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Commander Legends Tokens",
    "SetId": "tcmr",
    "Lang": ['en']
},
{ 
    "SetName": "Kaldheim",
    "SetId": "khm",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Kaldheim Promos",
    "SetId": "pkhm",
    "Lang": ['en']
},
{ 
    "SetName": "Kaldheim Tokens",
    "SetId": "tkhm",
    "Lang": ['en']
},
{ 
    "SetName": "Kaldheim Minigames",
    "SetId": "mkhm",
    "Lang": ['en']
},
{ 
    "SetName": "Kaldheim Substitute Cards",
    "SetId": "skhm",
    "Lang": ['en']
},
{ 
    "SetName": "Kaldheim Commander",
    "SetId": "khc",
    "Lang": ['en', 'zhs', 'ja']
},
{ 
    "SetName": "Kaldheim Commander Tokens",
    "SetId": "tkhc",
    "Lang": ['en']
},
{ 
    "SetName": "Kaldheim Art Series",
    "SetId": "akhm",
    "Lang": ['en']
},
{ 
    "SetName": "Time Spiral Remastered",
    "SetId": "tsr",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Time Spiral Remastered Tokens",
    "SetId": "ttsr",
    "Lang": ['en']
},
{ 
    "SetName": "Strixhaven: School of Mages",
    "SetId": "stx",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Strixhaven Mystical Archive",
    "SetId": "sta",
    "Lang": ['en']
},
{ 
    "SetName": "Strixhaven: School of Mages Promos",
    "SetId": "pstx",
    "Lang": ['en']
},
{ 
    "SetName": "Strixhaven: School of Mages Tokens",
    "SetId": "tstx",
    "Lang": ['en']
},
{ 
    "SetName": "Strixhaven: School of Mages Minigames",
    "SetId": "mstx",
    "Lang": ['en']
},
{ 
    "SetName": "Strixhaven: School of Mages Substitute Cards",
    "SetId": "sstx",
    "Lang": ['en']
},
{ 
    "SetName": "Commander 2021",
    "SetId": "c21",
    "Lang": ['en']
},
{ 
    "SetName": "Commander 2021 Tokens",
    "SetId": "tc21",
    "Lang": ['en']
},
{ 
    "SetName": "Modern Horizons 2",
    "SetId": "mh2",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Modern Horizons 2 Promos",
    "SetId": "pmh2",
    "Lang": ['en']
},
{ 
    "SetName": "Modern Horizons 2 Tokens",
    "SetId": "tmh2",
    "Lang": ['en']
},
{ 
    "SetName": "Modern Horizons 2 Minigames",
    "SetId": "mmh2",
    "Lang": ['en']
},
{ 
    "SetName": "Modern Horizons 1 Timeshifts",
    "SetId": "h1r",
    "Lang": ['en']
},
{ 
    "SetName": "Adventures in the Forgotten Realms",
    "SetId": "afr",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Adventures in the Forgotten Realms Promos",
    "SetId": "pafr",
    "Lang": ['en']
},
{ 
    "SetName": "Adventures in the Forgotten Realms Tokens",
    "SetId": "tafr",
    "Lang": ['en']
},
{ 
    "SetName": "Forgotten Realms Commander",
    "SetId": "afc",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Forgotten Realms Commander Tokens",
    "SetId": "tafc",
    "Lang": ['en']
},
{ 
    "SetName": "Forgotten Realms Commander Display Commanders",
    "SetId": "oafc",
    "Lang": ['en']
},
{ 
    "SetName": "Adventures in the Forgotten Realms Minigames",
    "SetId": "mafr",
    "Lang": ['en']
},
{ 
    "SetName": "Adventures in the Forgotten Realms Art Series",
    "SetId": "aafr",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Midnight Hunt",
    "SetId": "mid",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Innistrad: Midnight Hunt Promos",
    "SetId": "pmid",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Midnight Hunt Tokens",
    "SetId": "tmid",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Midnight Hunt Substitute Cards",
    "SetId": "smid",
    "Lang": ['en']
},
{ 
    "SetName": "Midnight Hunt Commander",
    "SetId": "mic",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Midnight Hunt Commander Tokens",
    "SetId": "tmic",
    "Lang": ['en']
},
{ 
    "SetName": "Midnight Hunt Commander Display Commanders",
    "SetId": "omic",
    "Lang": ['en']
},
{ 
    "SetName": "Midnight Hunt Commander Art Series",
    "SetId": "amid",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow",
    "SetId": "vow",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Innistrad: Crimson Vow Promos",
    "SetId": "pvow",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow Tokens",
    "SetId": "tvow",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow Minigames",
    "SetId": "mvow",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow Substitute Cards",
    "SetId": "svow",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow Commander",
    "SetId": "voc",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Innistrad: Crimson Vow Commander Tokens",
    "SetId": "tvoc",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow Display Commanders",
    "SetId": "ovoc",
    "Lang": ['en']
},
{ 
    "SetName": "Innistrad: Crimson Vow Art Series",
    "SetId": "avow",
    "Lang": ['en']
},
]

onlyEnglishSets = [

{ 
    "SetName": "Magic 2013",
    "SetId": "m13",
    "Lang": ['en']
},
{ 
    "SetName": "Magic 2013 Promos",
    "SetId": "pm13",
    "Lang": ['en']
},
{ 
    "SetName": "Magic 2013 Tokens",
    "SetId": "tm13",
    "Lang": ['en']
},
{ 
    "SetName": "Planechase 2012",
    "SetId": "pc2",
    "Lang": ['en']
},
{ 
    "SetName": "Planechase 2012 Planes",
    "SetId": "opc2",
    "Lang": ['en']
},
{ 
    "SetName": "Avacyn Restored",
    "SetId": "avr",
    "Lang": ['en']
},
{ 
    "SetName": "Avacyn Restored Promos",
    "SetId": "pavr",
    "Lang": ['en']
},
{ 
    "SetName": "Avacyn Restored Tokens",
    "SetId": "tavr",
    "Lang": ['en']
},
{ 
    "SetName": "Open the Helvault",
    "SetId": "phel",
    "Lang": ['en']
},
{ 
    "SetName": "Duel Decks: Venser vs. Koth",
    "SetId": "ddi",
    "Lang": ['en']
},
{ 
    "SetName": "Duel Decks: Venser vs. Koth Tokens",
    "SetId": "tddi",
    "Lang": ['en']
},
{ 
    "SetName": "Dark Ascension",
    "SetId": "dka",
    "Lang": ['en']
},
{ 
    "SetName": "Dark Ascension Promos",
    "SetId": "pdka",
    "Lang": ['en']
},
{ 
    "SetName": "Dark Ascension Tokens",
    "SetId": "tdka",
    "Lang": ['en']
},

{ 
    "SetName": "Gatecrash",
    "SetId": "gtc",
    "Lang": ['en']
},
{ 
    "SetName": "Gatecrash Promos",
    "SetId": "pgtc",
    "Lang": ['en']
},
{ 
    "SetName": "Gatecrash Tokens",
    "SetId": "tgtc",
    "Lang": ['en']
},


{ 
    "SetName": "Duel Decks: Sorin vs. Tibalt",
    "SetId": "ddk",
    "Lang": ['en']
},
{ 
    "SetName": "Duel Decks: Sorin vs. Tibalt Tokens",
    "SetId": "tddk",
    "Lang": ['en']
},


{ 
    "SetName": "Dragon's Maze",
    "SetId": "dgm",
    "Lang": ['en']
},
{ 
    "SetName": "Dragon's Maze Promos",
    "SetId": "pdgm",
    "Lang": ['en']
},
{ 
    "SetName": "Dragon's Maze Tokens",
    "SetId": "tdgm",
    "Lang": ['en']
},


{ 
    "SetName": "Modern Masters",
    "SetId": "mma",
    "Lang": ['en']
},
{ 
    "SetName": "Modern Masters Tokens",
    "SetId": "tmma",
    "Lang": ['en']
},


{ 
    "SetName": "Magic 2014",
    "SetId": "m14",
    "Lang": ['en']
},
{ 
    "SetName": "Magic 2014 Promos",
    "SetId": "pm14",
    "Lang": ['en']
},
{ 
    "SetName": "Magic 2014 Tokens",
    "SetId": "tm14",
    "Lang": ['en']
},


{ 
    "SetName": "Duel Decks: Heroes vs. Monsters",
    "SetId": "ddl",
    "Lang": ['en']
},
{ 
    "SetName": "Duel Decks: Heroes vs. Monsters Tokens",
    "SetId": "tddl",
    "Lang": ['en']
},


{ 
    "SetName": "Theros",
    "SetId": "ths",
    "Lang": ['en']
},
{ 
    "SetName": "Theros Promos",
    "SetId": "pths",
    "Lang": ['en']
},
{ 
    "SetName": "Theros Tokens",
    "SetId": "tths",
    "Lang": ['en']
},
{ 
    "SetName": "Face the Hydra",
    "SetId": "tfth",
    "Lang": ['en']
},
{ 
    "SetName": "Theros Hero's Path",
    "SetId": "thp1",
    "Lang": ['en']
},


{ 
    "SetName": "Commander 2013",
    "SetId": "c13",
    "Lang": ['en']
},
{ 
    "SetName": "Commander 2013 Oversized",
    "SetId": "oc13",
    "Lang": ['en']
},


{ 
    "SetName": "Born of the Gods",
    "SetId": "bng",
    "Lang": ['en']
},
{ 
    "SetName": "Born of the Gods Promos",
    "SetId": "pbng",
    "Lang": ['en']
},
{ 
    "SetName": "Born of the Gods Tokens",
    "SetId": "tbng",
    "Lang": ['en']
},
{ 
    "SetName": "Battle the Horde",
    "SetId": "tbth",
    "Lang": ['en']
},
{ 
    "SetName": "Born of the Gods Hero's Path",
    "SetId": "thp2",
    "Lang": ['en']
},


{ 
    "SetName": "Duel Decks: Jace vs. Vraska",
    "SetId": "ddm",
    "Lang": ['en']
},
{ 
    "SetName": "Duel Decks: Jace vs. Vraska Tokens",
    "SetId": "tddm",
    "Lang": ['en']
},

]

recentSets = [

{ 
    "SetName": "Innistrad: Double Feature",
    "SetId": "dbl",
    "Lang": ['en']
},

{ 
    "SetName": "Alchemy: Innistrad",
    "SetId": "ymid",
    "Lang": ['en']
},

{ 
    "SetName": "Kamigawa: Neon Dynasty",
    "SetId": "neo",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Kamigawa: Neon Dynasty Promos",
    "SetId": "pneo",
    "Lang": ['en']
},
{ 
    "SetName": "Kamigawa: Neon Dynasty Tokens",
    "SetId": "tneo",
    "Lang": ['en']
},
{ 
    "SetName": "Alchemy: Kamigawa",
    "SetId": "yneo",
    "Lang": ['en']
},
{ 
    "SetName": "Kamigawa: Neon Dynasty Minigames",
    "SetId": "mneo",
    "Lang": ['en']
},
{ 
    "SetName": "Kamigawa: Neon Dynasty Substitute Cards",
    "SetId": "sneo",
    "Lang": ['en']
},
{ 
    "SetName": "Neon Dynasty Commander",
    "SetId": "nec",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Neon Dynasty Commander Tokens",
    "SetId": "tnec",
    "Lang": ['en']
},
{ 
    "SetName": "Neon Dynasty Art Series",
    "SetId": "aneo",
    "Lang": ['en']
},



{ 
    "SetName": "Streets of New Capenna",
    "SetId": "snc",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Streets of New Capenna Promos",
    "SetId": "psnc",
    "Lang": ['en']
},
{ 
    "SetName": "Streets of New Capenna Southeast Asia Tokens",
    "SetId": "ptsnc",
    "Lang": ['en']
},
{ 
    "SetName": "Streets of New Capenna Tokens",
    "SetId": "tsnc",
    "Lang": ['en']
},
{ 
    "SetName": "Alchemy: New Capenna",
    "SetId": "ysnc",
    "Lang": ['en']
},
{ 
    "SetName": "New Capenna Commander",
    "SetId": "ncc",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "New Capenna Commander Promos",
    "SetId": "pncc",
    "Lang": ['en']
},
{ 
    "SetName": "New Capenna Commander Tokens",
    "SetId": "tncc",
    "Lang": ['en']
},
{ 
    "SetName": "Streets of New Capenna Minigames",
    "SetId": "msnc",
    "Lang": ['en']
},
{ 
    "SetName": "New Capenna Art Series",
    "SetId": "asnc",
    "Lang": ['en']
},


{ 
    "SetName": "Commander Legends: Battle for Baldur's Gate",
    "SetId": "clb",
    "Lang": ['en', 'ja', 'zhs', 'zht']
},
{ 
    "SetName": "Battle for Baldur's Gate Promos",
    "SetId": "pclb",
    "Lang": ['en']
},
{ 
    "SetName": "Battle for Baldur's Gate  Tokens",
    "SetId": "tclb",
    "Lang": ['en']
},
{ 
    "SetName": "Battle for Baldur's Gate Minigames",
    "SetId": "mclb",
    "Lang": ['en']
},
{ 
    "SetName": "Battle for Baldur's Gate Art Series",
    "SetId": "aclb",
    "Lang": ['en']
},

{ 
    "SetName": "Alchemy Horizons: Baldur's Gate",
    "SetId": "hbg",
    "Lang": ['en']
},


{ 
    "SetName": "Double Masters 2022",
    "SetId": "2x2",
    "Lang": ['en', 'ja', 'zhs']
},
{ 
    "SetName": "Double Masters 2022 Tokens",
    "SetId": "t2x2",
    "Lang": ['en']
},


{ 
    "SetName": "Dominaria United",
    "SetId": "dmu",
    "Lang": ['en', 'ja', 'zhs']
},
{ 
    "SetName": "Dominaria United Promos",
    "SetId": "pdmu",
    "Lang": ['en']
},
{ 
    "SetName": "Dominaria United Tokens",
    "SetId": "tdmu",
    "Lang": ['en']
},
{ 
    "SetName": "Dominaria United Art Series",
    "SetId": "admu",
    "Lang": ['en']
},
{ 
    "SetName": "Dominaria United Commander",
    "SetId": "dmc",
    "Lang": ['en', 'ja', 'zhs']
},
{ 
    "SetName": "Dominaria United Commander Tokens",
    "SetId": "tdmc",
    "Lang": ['en']
},

{ 
    "SetName": "Alchemy: Dominaria",
    "SetId": "ydmu",
    "Lang": ['en']
},


{ 
    "SetName": "Warhammer 40,000 Commander",
    "SetId": "40k",
    "Lang": ['en']
},
{ 
    "SetName": "Warhammer 40,000 Commander Tokens",
    "SetId": "t40k",
    "Lang": ['en']
},


{ 
    "SetName": "Unfinity",
    "SetId": "unf",
    "Lang": ['en']
},
{ 
    "SetName": "Unfinity Tokens",
    "SetId": "tunf",
    "Lang": ['en']
},
{ 
    "SetName": "Unfinity Sticker Sheets",
    "SetId": "sunf",
    "Lang": ['en']
},


{ 
    "SetName": "Game Night: Free-for-All",
    "SetId": "gn3",
    "Lang": ['en']
},
{ 
    "SetName": "Game Night: Free-for-All Tokens",
    "SetId": "tgn3",
    "Lang": ['en']
},


{ 
    "SetName": "30th Anniversary Edition",
    "SetId": "30a",
    "Lang": ['en']
},
{ 
    "SetName": "30th Anniversary Play Promos",
    "SetId": "p30a",
    "Lang": ['en']
},
{ 
    "SetName": "30th Anniversary Tokens",
    "SetId": "t30a",
    "Lang": ['en']
},



{ 
    "SetName": "Jumpstart 2022",
    "SetId": "j22",
    "Lang": ['en']
},
{ 
    "SetName": "Jumpstart 2022 Front Cards",
    "SetId": "fj22",
    "Lang": ['en']
},


{ 
    "SetName": "The Brothers' War",
    "SetId": "bro",
    "Lang": ['en', 'zhs', 'ja']
},
{ 
    "SetName": "The Brothers' War Retro Artifacts",
    "SetId": "brr",
    "Lang": ['en', 'zhs', 'ja']
},
{ 
    "SetName": "Transformers",
    "SetId": "bot",
    "Lang": ['en']
},
{ 
    "SetName": "Transformers Tokens",
    "SetId": "tbot",
    "Lang": ['en']
},
{ 
    "SetName": "The Brothers' War Promos",
    "SetId": "pbro",
    "Lang": ['en']
},
{ 
    "SetName": "The Brothers' War Tokens",
    "SetId": "tbro",
    "Lang": ['en']
},
{ 
    "SetName": "Alchemy: The Brothers' War",
    "SetId": "ybro",
    "Lang": ['en']
},
{ 
    "SetName": "The Brothers' War Commander",
    "SetId": "brc",
    "Lang": ['en', 'zhs', 'ja']
},
{ 
    "SetName": "The Brothers' War Commander Tokens",
    "SetId": "tbrc",
    "Lang": ['en']
},
{ 
    "SetName": "The Brothers' War Art Series",
    "SetId": "abro",
    "Lang": ['en']
},



{ 
    "SetName": "Starter Commander Decks",
    "SetId": "scd",
    "Lang": ['en']
},


{ 
    "SetName": "Dominaria Remastered",
    "SetId": "dmr",
    "Lang": ['en']
},
{ 
    "SetName": "Dominaria Remastered Tokens",
    "SetId": "tdmr",
    "Lang": ['en']
},


{ 
    "SetName": "Phrexia: All Will Be One",
    "SetId": "one",
    "Lang": ['en']
},
{ 
    "SetName": "Phrexia: All Will Be One Promos",
    "SetId": "pone",
    "Lang": ['en']
},
{ 
    "SetName": "Phrexia: All Will Be One Tokens",
    "SetId": "tone",
    "Lang": ['en']
},
{ 
    "SetName": "Phrexia: All Will Be One Commander",
    "SetId": "onc",
    "Lang": ['en']
},
{ 
    "SetName": "Phrexia: All Will Be One Commander Tokens",
    "SetId": "tonc",
    "Lang": ['en']
},
{ 
    "SetName": "Phrexia: All Will Be One Jumpstart Front Cards",
    "SetId": "fone",
    "Lang": ['en']
},
]


##################################################################


toBeCheckedSets = [



]


def main():
    for setConfig in toBeCheckedSets:
        for lang in setConfig['Lang']:
            check_set(setConfig['SetId'], lang)
        print('#' * 60)


if __name__ == '__main__':
    main()
