
from bc_api import BC_API

class Cache():

    robots = {}
    members = {}
    __api = None

    def init():
        Cache.__api = BC_API()
        Cache.__api.login()
        Cache.robots = Cache.__api.get_all_robots()
        Cache.members = Cache.__api.get_all_members()

    def update():
        Cache.robots = Cache.__api.get_all_robots()
        Cache.members = Cache.__api.get_all_members()

    def get_user_true_name(u_id):
        if not len(Cache.members):
            Cache.init()
        for m in Cache.members:
            if m.get("id") == u_id:
                return m.get("full_name")

        return "anonymous"

    def get_robot_true_name(r_id):
        if not len(Cache.robots):
            Cache.init()
        for m in Cache.robots:
            if m.get("id") == r_id:
                return m.get("name")

        return "anonymous"

    def check_is_robot(r_id):
        for i, r in Cache.robots.items():
            if r.get("id") == r_id:
                return True

        return False



