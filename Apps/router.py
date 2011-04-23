class AppsRouter(object):
    '''A router to control all database operations on models in
    Gammu application '''
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'Apps':
            return 'Apps'
        return None
