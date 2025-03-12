import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import os


def process_nine_grid_pinjie(image_filepathes, 
    output_image_dirpath, setId, saveAsJpg=True):
    

    w = 736                      # 每张小图片的宽度
    h = 1024                     # 每张小图片的高度
    IMAGE_ROW = 3                # 合成后图片一共有几行小图片
    IMAGE_COLUMN = 3             # 合成后图片一共有几列小图片

    # 通过留白将每张卡牌调整为 66mm * 91mm 的卡套
    delta_w = 68
    # delta_w = 72
    pinjie_w = w*3 + delta_w*4

    delta_h = 110
    # delta_h = 120
    pinjie_h = h*3 + delta_h*4

    # pinjie_w / pinjie_h => 297 / 210  A4纸尺寸
    
    # output_image_dirpath 合成后图片的存储目录 （可能有多张，每张一共 ROW*COLUMN 个小图片）
     
    # 定义图像拼接函数
    def image_compose(input_image_filepathes, output_image_filepath):
        to_image = Image.new(mode='RGBA', size=(pinjie_w, pinjie_h), color=(255, 255, 255)) #创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        dh = delta_h
        for y in range(1, IMAGE_ROW + 1):
            dw = delta_w
            for x in range(1, IMAGE_COLUMN + 1):
                if (IMAGE_COLUMN * (y - 1) + x - 1) < len(input_image_filepathes):
                    print(input_image_filepathes[IMAGE_COLUMN * (y - 1) + x - 1])
                    from_image = Image.open(input_image_filepathes[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                        (w, h), Image.ANTIALIAS)
                    to_image.paste(from_image, ((x - 1) * (w+delta_w) + dw, (y - 1) * (h+delta_h) + dh))
        
        draw = ImageDraw.Draw(to_image)

        # 画横线
        dw, dh = delta_w, delta_h
        line_width=3
        draw.line(((0, dh), (pinjie_w, dh)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, dh + h), (pinjie_w, dh + h)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, 2*dh + h), (pinjie_w, 2*dh + h)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, 2*dh + 2*h), (pinjie_w, 2*dh + 2*h)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, 3*dh + 2*h), (pinjie_w, 3*dh + 2*h)), fill=(0, 0, 0), width=line_width)
        draw.line(((0, 3*dh + 3*h), (pinjie_w, 3*dh + 3*h)), fill=(0, 0, 0), width=line_width)

        # 画竖线
        draw.line(((dw, 0), (dw, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((dw + w, 0), (dw + w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((2*dw + w, 0), (2*dw + w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((2*dw + 2*w, 0), (2*dw + 2*w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((3*dw + 2*w, 0), (3*dw + 2*w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((3*dw + 3*w, 0), (3*dw + 3*w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        draw.line(((4*dw + 3*w, 0), (4*dw + 3*w, pinjie_h)), fill=(0, 0, 0), width=line_width)


        # dw, dh = int(delta_w/2), int(delta_h/2)
        # line_width=3
        # draw.line(((0, dh), (pinjie_w, dh)), fill=(0, 0, 0), width=line_width)
        # draw.line(((0, dh + h), (pinjie_w, dh + h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((0, 3*dh + h), (pinjie_w, 3*dh + h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((0, 3*dh + 2*h), (pinjie_w, 3*dh + 2*h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((0, 5*dh + 2*h), (pinjie_w, 5*dh + 2*h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((0, 5*dh + 3*h), (pinjie_w, 5*dh + 3*h)), fill=(0, 0, 0), width=line_width)

        # # 画竖线
        # draw.line(((dw, 0), (dw, pinjie_h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((dw + w, 0), (dw + w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((3*dw + w, 0), (3*dw + w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((3*dw + 2*w, 0), (3*dw + 2*w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((5*dw + 2*w, 0), (5*dw + 2*w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((5*dw + 3*w, 0), (5*dw + 3*w, pinjie_h)), fill=(0, 0, 0), width=line_width)
        # draw.line(((7*dw + 3*w, 0), (7*dw + 3*w, pinjie_h)), fill=(0, 0, 0), width=line_width)

        if saveAsJpg:
            new_to_image = to_image.convert('RGB')
            new_to_image.save(output_image_filepath.replace('.png', '.jpg'), 
                format='JPEG', subsampling=0, quality=100)
        else:
            to_image.save(output_image_filepath) # 保存新图


    batch_size = IMAGE_ROW * IMAGE_COLUMN
    index = 0
    cnt = 0
    while index < len(image_filepathes):
        cnt += 1
        output_image_filepath = os.path.join(output_image_dirpath, "%s_%03d.png" % (setId, cnt))
        image_compose(image_filepathes[index : index+batch_size], output_image_filepath)
        index += batch_size


def process(input_image_dirpath, output_image_dirpath, setId):
    # input_image_dirpath 输入图片集地址
    # 获取全部小图片的路径地址
    image_filepathes = list()
    for image_filename in os.listdir(input_image_dirpath):
        image_filepathes.append(os.path.join(input_image_dirpath, image_filename))

    process_nine_grid_pinjie(image_filepathes, output_image_dirpath, setId)


def process_en_sm():
    DIR_PATH = '../card_database/Sun & Moon'
    OUPUT_PINJIE_DIRPATH = '../nine_grid_pinjie'
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'DET/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='DET')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'DRM/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='DRM')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'HIF/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='HIF')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SLG/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SLG')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SMP/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SMP')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'BUS/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='BUS')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'CEC/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CEC')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'CES/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CES')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'CIN/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CIN')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'FLI/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='FLI')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'GRI/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='GRI')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'LOT/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='LOT')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SUM/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SUM')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'TEU/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='TEU')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'UNB/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='UNB')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'UNM/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='UNM')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'UPR/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='UPR') 


def process_en_tt():
    DIR_PATH = '../card_database/Sword & Shield'
    OUPUT_PINJIE_DIRPATH = '../nine_grid_pinjie'
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'ASR/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='ASR')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'BRS/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='BRS')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'BST/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='BST')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'CEL/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CEL')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'CPA/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CPA')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'CRE/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='CRE')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'DAA/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='DAA')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'EVS/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='EVS')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'FST/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='FST')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'LOR/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='LOR')
    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'PGO/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='PGO')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'RCL/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='RCL')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SHF/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SHF')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SIT/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SIT')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SSH/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SSH')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'SSP/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='SSP')

    process(input_image_dirpath=os.path.join(DIR_PATH, 'VIV/img'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='VIV') 


def process_zhs():
    DIR_PATH = '../card_database'
    OUPUT_PINJIE_DIRPATH = '../zhs_nine_grid_pinjie'

    
    process(input_image_dirpath=os.path.join(DIR_PATH, 'zhs'), 
        output_image_dirpath=OUPUT_PINJIE_DIRPATH, setId='zhs')


def main():
    process_zhs()

    # process_en_sm()
    # process_en_tt()


if __name__ == "__main__":
    main()
