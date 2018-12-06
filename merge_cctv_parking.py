import xml.etree.ElementTree as Et
from PIL import Image
import shutil
import random
import os
import glob

SEP = '/'
ROOT = '/Users/kevin/Desktop/DS'
IN_CCTV_DIR = SEP.join([ROOT, 'cctv'])
IN_PARKING_DIRS = [SEP.join([ROOT, 'parking', 'img_gt_%d' % val]) for val in range(1, 7)]
OUT_ROOT_DIR = SEP.join([ROOT, 'cctv+parking'])
OUT_TMP_DIR = SEP.join([OUT_ROOT_DIR, 'temp'])
OUT_IMG_DIR = SEP.join([OUT_ROOT_DIR, 'train', 'images'])
OUT_XML_DIR = SEP.join([OUT_ROOT_DIR, 'train', 'annotations'])
OUT_VAL_IMG_DIR = SEP.join([OUT_ROOT_DIR, 'validation', 'images'])
OUT_VAL_XML_DIR = SEP.join([OUT_ROOT_DIR, 'validation', 'annotations'])


def rebuild_output_tree():
    if os.path.exists(OUT_ROOT_DIR):
        shutil.rmtree(OUT_ROOT_DIR)
    os.mkdir(OUT_ROOT_DIR)
    os.mkdir(OUT_TMP_DIR)
    os.mkdir(SEP.join([OUT_ROOT_DIR, 'train']))
    os.mkdir(OUT_IMG_DIR)
    os.mkdir(OUT_XML_DIR)
    os.mkdir(SEP.join([OUT_ROOT_DIR, 'validation']))
    os.mkdir(OUT_VAL_IMG_DIR)
    os.mkdir(OUT_VAL_XML_DIR)


def copy_cctv():
    os.chdir(IN_CCTV_DIR)
    for file in glob.glob('*.png'):
        name = file[:file.rindex('.')]
        path = SEP.join([IN_CCTV_DIR, '%s.xml' % name])
        if os.path.exists(path):
            shutil.copy(SEP.join([IN_CCTV_DIR, file]), SEP.join([OUT_TMP_DIR, file]))
            shutil.copy(path, SEP.join([OUT_TMP_DIR, '%s.xml' % name]))


def copy_parking():
    for IN_PARKING_DIR in IN_PARKING_DIRS:
        os.chdir(IN_PARKING_DIR)
        for file in glob.glob('*.jpg'):
            name = file[:file.rindex('.')]
            txt_path = SEP.join([IN_PARKING_DIR, '%s.txt' % name])
            if os.path.exists(txt_path):
                im_path = SEP.join([OUT_TMP_DIR, '%s.png' % file[:file.rindex('.')]])
                shutil.copy(SEP.join([IN_PARKING_DIR, file]), im_path)
                width, height = [str(val) for val in Image.open(im_path).size]
                with open(txt_path, 'r', encoding='KOI8-R') as r:
                    xmin, ymin, dx, dy = r.readline()[:-1].split(' ')
                    xmax, ymax = str(int(xmin) + int(dx)), str(int(ymin) + int(dy))
                gen_xml(
                    pfolder_path=OUT_TMP_DIR,
                    im_path=im_path,
                    im_file_name=name,
                    width=width,
                    height=height,
                    xmin=xmin,
                    xmax=xmax,
                    ymin=ymin,
                    ymax=ymax
                )


def gen_xml(pfolder_path, im_path, im_file_name, width, height, xmin, xmax, ymin, ymax):
    xml_path = SEP.join([pfolder_path, '%s.xml' % im_file_name])
    if os.path.exists(xml_path):
        _root = Et.parse(xml_path).getroot()
        _object = Et.Element('object')
        _name = Et.Element('name')
        _name.text = 'plate'
        _object.append(_name)
        _pose = Et.Element('pose')
        _pose.text = 'Unspecified'
        _object.append(_pose)
        _truncated = Et.Element('truncated')
        _truncated.text = '0'
        _object.append(_truncated)
        _difficult = Et.Element('difficult')
        _difficult.text = '0'
        _object.append(_difficult)
        _bndbox = Et.Element('bndbox')
        _xmin = Et.Element('xmin')
        _xmin.text = xmin
        _bndbox.append(_xmin)
        _ymin = Et.Element('ymin')
        _ymin.text = ymin
        _bndbox.append(_ymin)
        _xmax = Et.Element('xmax')
        _xmax.text = xmax
        _bndbox.append(_xmax)
        _ymax = Et.Element('ymax')
        _ymax.text = ymax
        _bndbox.append(_ymax)
        _object.append(_bndbox)
        _root.append(_object)
    else:
        _root = Et.Element('annotation')
        _root.set('verified', 'yes')
        _folder = Et.Element('folder')
        _folder.text = 'train'
        _root.append(_folder)
        _filename = Et.Element('filename')
        _filename.text = '%s.png' % im_file_name
        _root.append(_filename)
        _path = Et.Element('path')
        _path.text = im_path
        _root.append(_path)
        _source = Et.Element('source')
        _database = Et.Element('database')
        _database.text = 'Unknown'
        _source.append(_database)
        _root.append(_source)
        _size = Et.Element('size')
        _width = Et.Element('width')
        _width.text = width
        _size.append(_width)
        _height = Et.Element('height')
        _height.text = height
        _size.append(_height)
        _depth = Et.Element('depth')
        _depth.text = '3'
        _size.append(_depth)
        _root.append(_size)
        _segmented = Et.Element('segmented')
        _segmented.text = '0'
        _root.append(_segmented)
        _object = Et.Element('object')
        _name = Et.Element('name')
        _name.text = 'plate'
        _object.append(_name)
        _pose = Et.Element('pose')
        _pose.text = 'Unspecified'
        _object.append(_pose)
        _truncated = Et.Element('truncated')
        _truncated.text = '0'
        _object.append(_truncated)
        _difficult = Et.Element('difficult')
        _difficult.text = '0'
        _object.append(_difficult)
        _bndbox = Et.Element('bndbox')
        _xmin = Et.Element('xmin')
        _xmin.text = xmin
        _bndbox.append(_xmin)
        _ymin = Et.Element('ymin')
        _ymin.text = ymin
        _bndbox.append(_ymin)
        _xmax = Et.Element('xmax')
        _xmax.text = xmax
        _bndbox.append(_xmax)
        _ymax = Et.Element('ymax')
        _ymax.text = ymax
        _bndbox.append(_ymax)
        _object.append(_bndbox)
        _root.append(_object)
    with(open(xml_path, 'w')) as w:
        _result = str(Et.tostring(_root))
        w.writelines([_result[2:-1]])


def debug_outputs():
    bug_count = 0
    os.chdir(OUT_TMP_DIR)
    for file in glob.glob('*.xml'):
        with open(SEP.join([OUT_TMP_DIR, file]), 'r') as r:
            data = ''.join(r)
            while 'xmin' in data:
                xmin = int(data[data.index('<xmin>') + 6:data.index('</xmin>')])
                xmax = int(data[data.index('<xmax>') + 6:data.index('</xmax>')])
                ymin = int(data[data.index('<ymin>') + 6:data.index('</ymin>')])
                ymax = int(data[data.index('<ymax>') + 6:data.index('</ymax>')])
                data = data[data.index('</ymax>') + 7:]
                if xmax - xmin <= 0 or ymax - ymin <= 0:
                    os.remove(SEP.join([OUT_TMP_DIR, file]))
                    os.remove(SEP.join([OUT_TMP_DIR, '%s.png' % file[:file.rindex('.')]]))
                    bug_count += 1
                    break
    print('%d bugs found and removed' % bug_count)


def distribute():
    os.chdir(OUT_TMP_DIR)
    files = glob.glob('*.png')
    random.shuffle(files)
    val_cnt = int((len(files) / 2) * 0.2)

    for file in files:
        if val_cnt > 0:
            val_cnt -= 1
            shutil.move(
                SEP.join([OUT_TMP_DIR, file]),
                SEP.join([OUT_VAL_IMG_DIR, file]))
            shutil.move(
                SEP.join([OUT_TMP_DIR, '%s.xml' % file[:file.rindex('.')]]),
                SEP.join([OUT_VAL_XML_DIR, '%s.xml' % file[:file.rindex('.')]]))
        else:
            shutil.move(
                SEP.join([OUT_TMP_DIR, file]),
                SEP.join([OUT_IMG_DIR, file]))
            shutil.move(
                SEP.join([OUT_TMP_DIR, '%s.xml' % file[:file.rindex('.')]]),
                SEP.join([OUT_XML_DIR, '%s.xml' % file[:file.rindex('.')]]))
    os.rmdir(OUT_TMP_DIR)


if __name__ == '__main__':
    print('rebuilding the output tree')
    rebuild_output_tree()
    print('copying cctv dataset')
    copy_cctv()
    print('copying parking dataset')
    copy_parking()
    print('debugging merged output')
    debug_outputs()
    print('distributing dataset to train and validation sets')
    distribute()
