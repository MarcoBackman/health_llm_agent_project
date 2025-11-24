import time

class UidGenerator:
    @staticmethod
    def generate_uid():
        return str(int(round(time.time() * 1000)))

    @staticmethod
    def generate_agent_uid(key):
        return "agent_".join(key)