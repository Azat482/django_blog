from genericpath import exists
import os
import datetime
from django.conf import settings

class FileManager:
    def __init__(self):
        pass

    def UploadMediaFile(self, file, path, name_of_file):
        try:
            media_root = settings.MEDIA_ROOT
            media_url = 'media'
            full_path = "%s/%s" % (media_root, path)
            print('FULLPATH: ', full_path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            save_path = "%sfile%s" % (full_path, name_of_file)
            with open(save_path, 'wb+') as dest: 
                for part in file:
                    dest.write(part)
            return save_path.replace(media_root, media_url) #without MEDIA_ROOT path
        except Exception as e:
            print(e)
            return e        
