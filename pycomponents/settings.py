from environs import Env

env = Env()
env.read_env()

OSV_CACHE_SIZE: int = env.int("OSV_CACHE_SIZE", 1024)
OSV_CACHE_TTL: int = env.int("OSV_CACHE_TTL", 3600)
OSV_TIMEOUT: int = env.int("OSV_TIMEOUT", 30)


CVE_SEARCH_CACHE_SIZE: int = env.int("CVE_SEARCH_CACHE_SIZE", 1024)
CVE_SEARCH_CACHE_TTL: int = env.int("CVE_SEARCH_CACHE_TTL", 3600)
CVE_SEARCH_TIMEOUT: int = env.int("CVE_SEARCH_TIMEOUT", 30)
