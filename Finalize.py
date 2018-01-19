#! /usr/bin/env python
#! -*- coding: utf-8 -*-
import os, hashlib
from xml_formatter import Generate_XML

class FinalizeVideo:

    def __init__(self, retry_limit):
        self.img_server_path = None
        self.RETRY_LIMIT = retry_limit

    def DownloadAndStoreImage(self, image_url, video_url, IMAGE_DIR, IMAGE_THUMBNAIL_DIR, SOURCE, image_tolerance, XML_DIR, title, published_date, description):
        # Image Name
        img_name = self.createMD5hash(image_url)
        img_extension = image_url.split('.')[-1].split('?')[0]
        img_name = img_name + "." + img_extension

        image_store_path = IMAGE_DIR + SOURCE
        # Fetch image in respective folder
        state = self.fetchImage(image_url, image_store_path, img_name)
        if state == False and image_tolerance == "False":
            print("Image Not avaialbe: skipping ", video_url)
            return "Error"
        else:
            self.img_server_path = IMAGE_THUMBNAIL_DIR + SOURCE + "/" + img_name
            self.Generate_XML_FILE(XML_DIR,SOURCE, title, published_date, description, video_url, self.img_server_path, image_store_path + "/" + img_name)


    def fetchImage(self, image_url, dst, img_name):
        _error = True
        counter = 0
        try:
            if not os.path.isdir(dst):
                print("WARN:Creating directory : %s" % (dst))
                os.makedirs(dst)
        except Exception as e:
            print(e)

        while _error and counter < self.RETRY_LIMIT:
            try:
                command = "wget %s -O %s" % (image_url, dst + '/' + img_name)
                os.system(command)
                _error = False
            except Exception as err:
                counter = counter + 1
                _error = True
                print("ImageFetchError: %s\t%s" % (image_url, err))

        if _error:
            return False
        else:
            return True

    def createMD5hash(self, url):
        url = url.encode("utf-8")
        hash_object = hashlib.md5(url)
        unique_key = hash_object.hexdigest()
        return unique_key

    def generate_xml_directory(self, xml_path):
        try:
            if not os.path.isdir(xml_path):
                print("WARN:Creating directory : %s" % (xml_path))
                os.makedirs(xml_path)
                return True
            else:
                print("Already a Directory")
                return True
        except Exception as e:
            print(e)
            return False

    def Generate_XML_FILE(self, XML_DIR, SOURCE, title, published_date, description, video_url, img_server_path, image_store_path):
        xml_path = XML_DIR + SOURCE
        group = "ur_videos"
        if self.generate_xml_directory(xml_path):
            Generate_XML(title, video_url, group, img_server_path, outDir= xml_path,
                                 text= description, date=published_date, tag="یوٹیوب", img_store_path=image_store_path)