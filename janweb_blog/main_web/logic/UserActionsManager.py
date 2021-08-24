import datetime
from django.contrib.auth.models import User

class UserActionsManager:
    def __init__(self, user):
        self.user = user

    #set likes and dislikes
    def SetRatingItemToObject(self, LikeModel, DislikeModel, OwnerObject, method, obj_id):
        user = self.user
        try:
            if method == 'like':
                like_already_exist = LikeModel.objects.filter(user = user, owner_object = obj_id) 
                if like_already_exist.exists():
                    like_already_exist.delete()
                else:
                    like_article  = LikeModel()
                    like_article.user = user
                    like_article.datetime_creating = datetime.datetime.now()
                    like_article.owner_object = OwnerObject.objects.get(id = obj_id)
                    like_article.save()
                    DislikeModel.objects.filter(user = user, owner_object = obj_id).delete()
                return True
            if method == 'dislike':
                dislike_already_exist = DislikeModel.objects.filter(user = user, owner_object = obj_id)
                if dislike_already_exist.exists():
                    dislike_already_exist.delete()
                else:
                    dislike_article = DislikeModel()
                    dislike_article.user = user
                    dislike_article.datetime_creating = datetime.datetime.now()
                    dislike_article.owner_object = OwnerObject.objects.get(id = obj_id)
                    dislike_article.save()
                    LikeModel.objects.filter(user = user, owner_object = obj_id).delete()
                return True
            else:
                return False
        except Exception as e:
            print(type(e))
            print(e)
            return False

    def AddCommentToObject(self, CommentModel, OwnerObject, text, obj_id):
        user = self.user
        try:
            comment = CommentModel()
            comment.user = user
            comment.owner_object = OwnerObject.objects.get(id = obj_id)
            comment.datetime_creating = datetime.datetime.now()
            comment.comment_text = text
            comment.save()
            return True
        except Exception as e:
            print(e)
            return False
    
