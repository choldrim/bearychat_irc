
from lib.bc_api import BC_API

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

        somebody = "somebody"

        for m in Cache.members:
            if m.get("id") == u_id:
                name = m.get("full_name")
                if not name:
                    return somebody
                if not name.strip():
                    return somebody
                return name

        return somebody


    def get_user_en_name(u_id):
        name = Cache.get_user_true_name(u_id)

        # check ascii name
        if all(ord(c) < 128 for c in name):
            return name
        else:
            m = None
            for _m in Cache.members:
                if _m.get("id") == u_id:
                     m = _m
            if not m:
                return "somebody"
            email = m.get("email")
            if email:
                name = email.split("@")[0]
                return name
            else:
                return "somebody"


    def get_robot_true_name(r_id):
        if not len(Cache.robots):
            Cache.init()
        for m in Cache.robots:
            if m.get("id") == r_id:
                return m.get("name")

        return "somebody"


    def check_is_robot(r_id):
        for i, r in Cache.robots.items():
            if r.get("id") == r_id:
                return True

        return False

