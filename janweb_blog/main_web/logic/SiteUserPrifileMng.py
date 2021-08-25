from ..models import UserProfile
from django.contrib.auth.models import User
from itertools import chain
from .FileManager import FileManager
import datetime
import os

class ProfileDataManage:
        #structure data to send 
        class ProfileStructData: 
            def __init__(self, profile):
                self.username = profile.user
                self.avatar_url = profile.avatar_url
                self.date_registration = profile.date_registration
                self.likes = profile.user_likes_count
                self.dislikes = profile.user_dislikes_count
                self.articles = profile.user_articles_count
                self.comments  = profile.user_comments_count

            def __str__(self):
                data_list = [
                    'USERNAME: ', str(self.username),
                    '\n',
                    'DATE RAGISTRATION: ', str(self.date_registration),
                    ]
                string_data = ''
                for str_part in data_list:
                    string_data += str_part
                return string_data

        def __init__(self, req):
            self.user = User.objects.get(username = req.user)
            try:
                self.profile = UserProfile.objects.get(user = self.user)
            except UserProfile.DoesNotExist as e:
                self.profile = self.CreateProfile(self.user)
                   
        def GetProfileData(self):
            return self.ProfileStructData(self.profile)
            
        def CreateProfile(self, user):
            profile = UserProfile()
            profile.user = user
            profile.date_registraton = datetime.datetime.now()
            profile.save()
            return profile

        def SetAvatarProfile(self, img):
            try:
                path = 'users-media/images/avatar/'
                exeption = os.path.splitext(img.name)[1]
                name = ("_image_ava%s%s" % (str(datetime.datetime.now()), exeption)).replace(' ', '')
                upload = FileManager().UploadMediaFile(img, path, name)
                print('IMAGE PATH GETTING FROM UPLOADER: ', upload)
                self.profile.avatar_url = upload
                self.profile.save()
                return True
            except Exception as e:
                print('SETAVAERR: ', e)
                return False

        def GetProfileAvatar(self):
            return self.profile.avatar_url
        
        def UpdateStatistic(self):
            Profile = self.profile
            User = self.user
            Profile.user_articles_count = User.article_set.all().count()
            Profile.user_comments_count = User.commentarticle_set.all().count()         
            Profile.user_likes_count = User.likearticle_set.all().count()
            Profile.user_dislikes_count = User.dislikearticle_set.all().count()
            Profile.save()
        
