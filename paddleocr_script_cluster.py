from paddleocr import PaddleOCR, draw_ocr
import os
import glob
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # need to run only once to download and load model into memory
img_path = './img_input'

targeted_box_cshot = [[3285.0, 772.0], [3450.0, 784.0], [3444.0, 865.0], [3279.0, 853.0]]
targeted_box_bf1shot = [[3285.0, 859.0], [3461.0, 859.0], [3461.0, 940.0], [3285.0, 940.0]]
targeted_box_bf2shot = [[3290.0, 936.0], [3461.0, 936.0], [3461.0, 1013.0], [3290.0, 1013.0]]


cshot_cycletime_hist = 0
bf1shot_cycletime_hist = 0
bf2shot_cycletime_hist = 0

targeted_box_INJ1stPS= [[1345.0, 773.0], [1525.0, 773.0], [1525.0, 855.0], [1345.0, 855.0]]
targeted_box_MTGready = [[2968.0, 778.0], [3140.0, 778.0], [3140.0, 855.0], [2968.0, 855.0]]
targeted_box_MTGtime = [[1632.0, 773.0], [1833.0, 773.0], [1833.0, 855.0], [1632.0, 855.0]]
targeted_box_INJendPOS = [[2651.0, 778.0], [2827.0, 778.0], [2827.0, 855.0], [2651.0, 855.0]]
targeted_box_MaxFWD = [[2339.0, 778.0], [2514.0, 778.0], [2514.0, 855.0], [2339.0, 855.0]]
targeted_box_INJready = [[1987.0, 778.0], [2197.0, 778.0], [2197.0, 855.0], [1987.0, 855.0]]
targeted_box_datetime = [[2669.0, 303.0], [3495.0, 303.0], [3495.0, 376.0], [2669.0, 376.0]]


shot_info = []
#Overlap calculation (box1 is ref)
def calculate_overlap(box1, box2):
    box1_x1, box1_y1, box1_x2, box1_y2 = box1[0][0], box1[0][1], box1[2][0], box1[2][1]
    box2_x1, box2_y1, box2_x2, box2_y2 = box2[0][0], box2[0][1], box2[2][0], box2[2][1]

    # Calculate overlap
    x_overlap = max(0, min(box1_x2, box2_x2) - max(box1_x1, box2_x1))
    y_overlap = max(0, min(box1_y2, box2_y2) - max(box1_y1, box2_y1))
    return x_overlap * y_overlap

#IoU calculation (box1 is ref)
def calculate_IoU(box1, box2):
    box1_x1, box1_y1, box1_x2, box1_y2 = box1[0][0], box1[0][1], box1[2][0], box1[2][1]
    box2_x1, box2_y1, box2_x2, box2_y2 = box2[0][0], box2[0][1], box2[2][0], box2[2][1]

    # Calculate overlap
    x_overlap = max(0, min(box1_x2, box2_x2) - max(box1_x1, box2_x1))
    y_overlap = max(0, min(box1_y2, box2_y2) - max(box1_y1, box2_y1))

    intersect_area = x_overlap * y_overlap
    union_area = (box1_x2 - box1_x1)*(box1_y2 - box1_y1) + (box2_x2 - box2_x1)*(box2_y2 - box2_y1) + - intersect_area
    return intersect_area / union_area

def find_files_by_prefix(directory, prefix):
    """
    Find files in a directory where the filename starts with the given prefix.

    Parameters:
    directory (str): The path to the directory to search.
    prefix (str): The prefix to search for.

    Returns:
    list: A list of paths to files that match the prefix.
    """
    # Construct the search pattern to match the prefix followed by any characters
    pattern = os.path.join(directory, f"{prefix}*")
    # print("******", pattern)
    # Use glob to find files matching the pattern
    matching_files = glob.glob(pattern)

    return matching_files

def txt2float(str_input):
    #replacing commas or apostrophes with a dot
    str_output = str_input.replace("'", ".").replace(",", ".")
    return float(str_output)

step =1216
while step < 4262:
# while step < 1418:

    max_overlap_cshot = 0
    max_overlap_bf1shot =0
    max_overlap_bf2shot = 0
    max_overlap_INJ1stPS = 0
    max_overlap_MTGready = 0
    max_overlap_MTGtime = 0
    max_overlap_INJendPOS = 0
    max_overlap_INJready = 0
    max_overlap_MaxFWD = 0
    max_overlap_datetime = 0
    files = find_files_by_prefix(img_path, "image_{:08}".format(step))
    # print("*******", files)
    if files:
        result_b = ocr.ocr(files[0], cls=True)
    else:
        print("No files starting with image_{:08}, by pass...".format(step))
        step = step + 1
        continue
    result = result_b[0]
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    for i, box in enumerate(boxes):
        overlap = calculate_IoU(targeted_box_cshot, box)
        if overlap > max_overlap_cshot:
            max_overlap_cshot = overlap
            index_cshot_cycletime = i
        overlap = calculate_IoU(targeted_box_bf1shot, box)
        if overlap > max_overlap_bf1shot:
            max_overlap_bf1shot = overlap
            index_bf1shot_cycletime = i
        overlap = calculate_IoU(targeted_box_bf2shot, box)
        if overlap > max_overlap_bf2shot:
            max_overlap_bf2shot = overlap
            index_bf2shot_cycletime = i
    cshot_cycletime = float(txts[index_cshot_cycletime])
    bf1shot_cycletime = float(txts[index_bf1shot_cycletime])
    bf2shot_cycletime = float(txts[index_bf2shot_cycletime])
    print("In file test{:03}.jpg, cshot_cycletime is {}, bf1shot_cycletime is {}, bf2shot_cycletime is {}".format(step, cshot_cycletime, bf1shot_cycletime, bf2shot_cycletime))
    if cshot_cycletime_hist == 0:
        cshot_cycletime_hist = cshot_cycletime
        bf1shot_cycletime_hist = bf1shot_cycletime
        bf2shot_cycletime_hist = bf2shot_cycletime
    elif cshot_cycletime_hist != cshot_cycletime or bf1shot_cycletime_hist != bf1shot_cycletime or bf2shot_cycletime_hist != bf2shot_cycletime:
        print("Latest shot data generated")
        cshot_cycletime_hist = cshot_cycletime
        bf1shot_cycletime_hist = bf1shot_cycletime
        bf2shot_cycletime_hist = bf2shot_cycletime
        for i, box in enumerate(boxes):
            overlap = calculate_IoU(targeted_box_INJ1stPS, box)
            if overlap > max_overlap_INJ1stPS:
                max_overlap_INJ1stPS = overlap
                index_INJ1stPS = i
            overlap = calculate_IoU(targeted_box_MTGtime, box)
            if overlap > max_overlap_MTGtime:
                max_overlap_MTGtime = overlap
                index_MTGtime = i
            overlap = calculate_IoU(targeted_box_INJready, box)
            if overlap > max_overlap_INJready:
                max_overlap_INJready = overlap
                index_INJready = i
            overlap = calculate_IoU(targeted_box_MaxFWD, box)
            if overlap > max_overlap_MaxFWD:
                max_overlap_MaxFWD = overlap
                index_MaxFWD = i
            overlap = calculate_IoU(targeted_box_INJendPOS, box)
            if overlap > max_overlap_INJendPOS:
                max_overlap_INJendPOS = overlap
                index_INJendPOS = i
            overlap = calculate_IoU(targeted_box_MTGready, box)
            if overlap > max_overlap_MTGready:
                max_overlap_MTGreeady = overlap
                index_MTGready = i
            overlap = calculate_IoU(targeted_box_datetime, box)
            if overlap > max_overlap_datetime:
                max_overlap_datetime = overlap
                index_datetime = i

        INJ1stPS = txt2float(txts[index_INJ1stPS])
        MTGtime = txt2float(txts[index_MTGtime])
        INJready = txt2float(txts[index_INJready])
        INJendPOS = txt2float(txts[index_INJendPOS])
        MTGready = txt2float(txts[index_MTGready])
        MaxFWD = txt2float(txts[index_MaxFWD])
        date_time = txts[index_datetime]
        shot_info.append([INJ1stPS, MTGtime, INJready, MaxFWD, INJendPOS, MTGready, cshot_cycletime, date_time])
    step = step + 1

import csv
# Open a CSV file for writing
with open('my_list.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the list to the CSV file
    writer.writerows(shot_info)

# 显示结果
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./StyleText/fonts/en_standard.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('./ppocr_imgs_test/result.jpg')
