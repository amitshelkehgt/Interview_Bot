import uuid
class utils:    
    session_id = None
    @staticmethod
    def get_session_id(sid=None):
        if utils.session_id == None:
            if sid==None:
                utils.session_id = str(uuid.uuid4())
            else:
                utils.session_id = sid
        else:
            return utils.session_id