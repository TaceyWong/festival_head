# coding:utf-8

from datetime import datetime
from PIL import Image,ImageDraw
import glob
import os
import uuid
import face_recognition
import numpy as np


class PicBase(object):

    def __init__(self,masks_path="./"):
        self._mask_list = tuple()
        self._masks_path = masks_path
        self._update_mask_list(masks_path=self._masks_path)

    @property
    def masks_path(self):
        return self._masks_path

    @masks_path.setter
    def masks_path(self,value):
        self._masks_path = value
        self._update_mask_list(masks_path = self._masks_path)


    @property
    def mask_list(self):
        return self._mask_list

    @mask_list.setter
    def mask_list(self,m_list):
        self.mask_list = self._update_mask_list(list_content=m_list)
    def _update_mask_list(self,**kw):
        m_list = []
        if kw.get("masks_path"):
            print kw.get("masks_path")
            self._masks_path = kw.get("masks_path")
            masks = glob.glob(self.masks_path+os.sep+"*_mask.png")
            for mask in masks:
                im = Image.open(mask).convert('RGBA')
                m_list.append(im)
        elif kw.get("list_content"):
            for mask in ke.get("list_content"):
                im = Image.open(mask).convert('RGBA')
                m_list.append(im)
        else:
            return False
        self._mask_list = tuple(m_list)
        return True

    def _gen_mask(self,ori,mask,res,start):
        mask = mask.resize(res, Image.ANTIALIAS)
        ori.paste(mask, start, mask=mask)
        return ori

    def _gen_name(self,store_path):
        pic_name = str(uuid.uuid4())+".png"
        pic_path = os.path.join(store_path,pic_name)
        return pic_path

    def _adap_img(self):
        pass

    def _load_img(self,ori):
        img = Image.open(ori).convert('RGBA')


class Festival(object):
    def __init__(self):
        self.zh_name = ""
        self.en_name = ""
        self.type = "zh"
        self.logo_list = []

class FestivalHead(PicBase):

    def __init__(self,masks_path="./"):
        super(FestivalHead,self).__init__(masks_path)
        self.pic_width = 0
        self.pic_height = 0

    def rec_face(self,pic):
        pic = pic.convert("L")
        img = np.array(pic)
        face_locations = face_recognition.face_locations(img)
        return face_locations

    def gen_face(self,ori,faces):
        result = []
        for face in faces:
            top,right,bottom,left = face
            width = right-left
            height = bottom-top
            r_w = int(width*1.2)
            r_h = int(min(top*1.2,r_w*1.0/self.mask_list[0].size[0]*self.mask_list[0].size[1]))
            start = (int(left-width*0.1),max(0,top-r_h))
            ori = self._gen_mask(ori,self.mask_list[0],(r_w,r_h),start)
        pic_path = self._gen_name(store_path="./")
        ori.save(pic_path)
        return pic_path



    def show_face(self,ori,faces):
        d = ImageDraw.Draw(ori)
        for face in faces:
            box = (face[3],face[0],face[1],face[2])
            d.rectangle(box,outline=(255,0,0))
        ori.show()


    def gen_no_face(self,ori):
        r_w = int(self.pic_width*0.8)
        r_h = int(min(self.pic_height*0.4*1.2,r_w*1.0/self.mask_list[0].size[0]*self.mask_list[0].size[1]))
        start = (int(0.1*self.pic_width),max(0,self.pic_height*0.2-r_h))
        ori = self._gen_mask(ori,self.mask_list[0],(r_w,r_h),start)
        pic_path = self._gen_name(store_path="./")
        ori.save(pic_path)
        return pic_path


    def gen(self,ori,mask_index=0):
        ori = Image.open(ori).convert('RGBA')
        self.pic_width,self.pic_height = ori.size
        print ori.size
        faces = self.rec_face(ori)
        if faces:
            pic_path = self.gen_face(ori,faces)
        else:
            pic_path = self.gen_no_face(ori)
        return pic_path
