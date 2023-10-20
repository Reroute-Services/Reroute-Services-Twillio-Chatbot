from datetime import timedelta, datetime
import uuid
import gc


class SessionManager:
    def __init__(self):
        self.CHAT_SESSIONS = {}
        self.expire_delta = 5
        self.gc_counter = 0
        self.gc_delay = 5
    
    def new_session(self, sender_id, session_context):
        # session_id = str(uuid.uuid4())
        session_id = sender_id
        self.CHAT_SESSIONS[session_id] = {
            "session_context": session_context,
            "exp": datetime.utcnow() + timedelta(minutes=self.expire_delta)
        }
        return (session_id, self.get_session_context(session_id))
    
    def get_session_context(self, session_id):
        self.CHAT_SESSIONS[session_id]["exp"] = datetime.utcnow() + timedelta(minutes=self.expire_delta)
        return self.CHAT_SESSIONS[session_id]["session_context"]
    
    def session_exists(self, session_id: str):
        return session_id in self.CHAT_SESSIONS.keys()
        
    def expirator(self, garbage_collection=True):
        delete_sessions_list = []
        current_time = datetime.utcnow()
        for session in self.CHAT_SESSIONS:
            if self.CHAT_SESSIONS[session]["exp"] <= current_time:
                delete_sessions_list.append(session)
        
        for session in delete_sessions_list:
            del self.CHAT_SESSIONS[session]
            self.gc_counter += 1
            print("[Session Manager] Successfully Deleted Session:",session)
        if garbage_collection and self.gc_counter >= self.gc_delay:
            print("[Session Manager] Garbage Collected: {} bytes".format(gc.collect()))
            self.gc_counter = 0
        print("[Session Manager] Currently Active Sessions:", len(self.CHAT_SESSIONS))

