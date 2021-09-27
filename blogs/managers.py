from tortoise.manager import Manager


class PostManager(Manager):
    def get_queryset():
        return super(PostManager, self).get_queryset()
    
class CategoryManager():
    def get_queryset():
        return super(PostManager, self).get_queryset()
