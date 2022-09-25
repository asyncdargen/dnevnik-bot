cache_file = "cache.txt"


def write_auth_cache(profile_id: str, auth_token: str):
    if len(cache_file) > 0:
        with open(cache_file, "w") as file:
            file.writelines([profile_id, "\n", auth_token, "\n"])


def read_auth_cache():
    if len(cache_file) > 0:
        try:
            with open(cache_file) as file:
                return file.read().splitlines()
        except:
            return None
    else:
        return None
