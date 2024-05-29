import os
import PIL
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw


class GridImagesDrawer(object):
    def __init__(self):
        self.A4_Width_mm =  210.0
        self.A4_Height_mm = 297.0
        self.left_corner_w = 16
        self.left_corner_h = 45

        self.A4_wh_ratio = self.A4_Width_mm / self.A4_Height_mm
        self.image_row_cnt = 3
        self.image_column_cnt = 3


    def draw(self, image_filepath_list, output_key,
             output_dirpath, isCardBack=False):

        origin_w = 745     # 每张小图片的宽度
        origin_h = 1040    # 每张小图片的高度
        w = origin_w
        h = int(w / self.A4_wh_ratio)
        IMAGE_ROW = self.image_row_cnt        # 合成后图片一共有几行小图片
        IMAGE_COLUMN = self.image_column_cnt  # 合成后图片一共有几列小图片

        margin_w = 120
        # (2 * margin_w + self.image_column_cnt * w) = (2 * margin_h + self.image_row_cnt * h) * self.A4_wh_ratio
        margin_h = int(((2 * margin_w + self.image_column_cnt * w) / self.A4_wh_ratio - self.image_row_cnt * h)/2)
        print(f'margin_w={margin_w}, margin_h={margin_h}')

        # 通过留白将每张卡牌调整为 66mm * 91mm 的卡套
        pinjie_w = w * self.image_column_cnt + 2*margin_w
        pinjie_h = h * self.image_row_cnt + 2*margin_h

        # output_image_dirpath 合成后图片的存储目录 （可能有多张，每张一共 ROW*COLUMN 个小图片）

        # 定义图像拼接函数
        def image_compose(input_image_filepathes, output_image_filepath, saveAsJPG=True):
            to_image = Image.new(mode='RGBA', size=(pinjie_w, pinjie_h), color=(255, 255, 255)) #创建一个新图
            # 循环遍历，把每张图片按顺序粘贴到对应位置上
            for y in range(1, IMAGE_ROW + 1):
                for x in range(1, IMAGE_COLUMN + 1):
                    if (IMAGE_COLUMN * (y - 1) + x - 1) < len(input_image_filepathes):
                        print(input_image_filepathes[IMAGE_COLUMN * (y - 1) + x - 1])

                        from_image =  Image.open(input_image_filepathes[IMAGE_COLUMN * (y - 1) + x - 1])
                        ow, oh = from_image.size
                        if ow != w or oh != h:
                            from_image = from_image.resize( (w, h), PIL.Image.Resampling.LANCZOS)
                        
                        if isCardBack:
                            to_image.paste(from_image, ((x - 1) * w + margin_w, (y - 1) * h + margin_h))
                        else:
                            cropped_img = from_image.crop((self.left_corner_w, 
                                                           self.left_corner_h,
                                                           self.left_corner_w + w,
                                                           self.left_corner_h + h))
                            to_image.paste(cropped_img, ((x - 1) * w + margin_w, (y - 1) * h + margin_h))
            
            draw = ImageDraw.Draw(to_image)

            # 画横线
            line_width=3
            for row in range(0, self.image_row_cnt+1):
                draw.line(((0, row * h + margin_h), (pinjie_w, row * h + margin_h)), fill=(0, 0, 0), width=line_width)

            # 画竖线
            for col in range(0, self.image_column_cnt+1):
                draw.line(((col * w + margin_w, 0), (col * w + margin_w, pinjie_h)), fill=(0, 0, 0), width=line_width)

            if saveAsJPG:
                new_to_image = to_image.convert('RGB')
                new_to_image.save(output_image_filepath.replace('.png', '.jpg'), 
                    format='JPEG', subsampling=0, quality=100)
            else:
                to_image.save(output_image_filepath) # 保存新图

        batch_size = IMAGE_ROW * IMAGE_COLUMN
        index = 0
        cnt = 0
        while index < len(image_filepath_list):
            cnt += 1
            output_image_filepath = os.path.join(output_dirpath, "%s_%03d.png" % (output_key, cnt))
            image_compose(image_filepath_list[index : index+batch_size], output_image_filepath)
            index += batch_size

