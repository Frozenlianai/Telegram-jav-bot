import os
import json
import redis
import typing
import logging
import threading

LOG = logging.getLogger(__name__)


class BotFileDb:
    def __init__(self, path_record_file: str):
        """初始化

        :param str path_record_file: 记录文件位置
        """
        self.path_record_file = path_record_file
        self._lock = threading.Lock()

    def check_has_record(self) -> typing.Tuple[dict, bool, bool]:
        """检查是否有收藏记录, 如果有则返回记录

        :return tuple[dict, bool, bool]: 收藏记录, 演员记录是否存在, 番号记录是否存在
        """
        # 初始化数据
        record = {}
        # 加载记录
        if os.path.exists(self.path_record_file):
            try:
                with open(self.path_record_file, "r", encoding="utf8") as f:
                    record = json.load(f)
            except Exception as e:
                LOG.error(f"加载收藏记录文件失败: {e}")
                return None, False, False
        # 尚无记录
        if not record or record == {}:
            return None, False, False
        # 检查并返回记录
        is_stars_exists = False
        is_avs_exists = False
        if (
            "stars" in record.keys()
            and record["stars"] != []
            and len(record["stars"]) > 0
        ):
            is_stars_exists = True
        if "avs" in record.keys() and record["avs"] != [] and len(record["avs"]) > 0:
            is_avs_exists = True
        return record, is_stars_exists, is_avs_exists

    def check_star_exists_by_id(self, star_id: str) -> bool:
        """根据演员 id 确认收藏记录中演员是否存在

        :param str star_id: 演员 id
        :return bool: 是否存在
        """
        record, exists, _ = self.check_has_record()
        if not record or not exists:
            return False
        stars = record["stars"]
        for star in stars:
            if star["id"].lower() == star_id.lower():
                return True

    def check_id_exists(self, id: str) -> bool:
        """根据番号确认收藏记录中番号是否存在

        :param str id: 番号
        :return bool: 是否存在
        """
        record, _, exists = self.check_has_record()
        if not record or not exists:
            return False
        avs = record["avs"]
        for av in avs:
            if av["id"].lower() == id.lower():
                return True

    def renew_record(self, record: dict) -> bool:
        """更新记录

        :param dict record: 新的记录
        :return bool: 是否更新成功
        """
        try:
            with self._lock, open(self.path_record_file, "w", encoding="utf8") as f:
                json.dump(
                    record, f, separators=(",", ": "), indent=4, ensure_ascii=False
                )
            return True
        except Exception as e:
            LOG.error(f"更新收藏记录文件失败: {e}")
            return False

    def get_groups(self) -> list:
        """获取所有群组"""
        record, _, _ = self.check_has_record()
        return record.get("groups", []) if record else []

    def add_group(self, group_id: int, title: str):
        """添加或更新群组"""
        record, _, _ = self.check_has_record()
        if not record:
            record = {}
        
        groups = record.get("groups", [])
        
        # 检查群组是否已存在
        group_exists = False
        for group in groups:
            if group["id"] == group_id:
                group["title"] = title  # 更新标题
                group_exists = True
                break
        
        if not group_exists:
            groups.append({"id": group_id, "title": title})
            
        record["groups"] = groups
        self.renew_record(record)

    def remove_group(self, group_id: int):
        """移除群组"""
        record, _, _ = self.check_has_record()
        if not record:
            return

        groups = record.get("groups", [])
        groups_to_keep = [g for g in groups if g.get("id") != group_id]
        
        if len(groups_to_keep) < len(groups):
            record["groups"] = groups_to_keep
            self.renew_record(record)

    def record_star_by_name_id(self, star_name: str, star_id: str) -> bool:
        """记录演员

        :param str star_name: 演员名称
        :param str star_id: 演员编号
        :return bool: 是否收藏成功
        """
        # 加载记录
        record, is_stars_exists, _ = self.check_has_record()
        if not record:
            record, stars = {}, []
        else:
            if not is_stars_exists:
                stars = []
            else:
                stars = record["stars"]
        # 检查记录是否存在
        for star in stars:
            if star["id"].lower() == star_id.lower():
                return True
        # 如果记录需要更新则写回记录
        stars.append({"name": star_name, "id": star_id.lower()})
        record["stars"] = stars
        return self.renew_record(record)

    def record_id_by_id_stars(self, id: str, stars: list) -> bool:
        """记录番号

        :param str id: 番号
        :param list stars: 演员编号列表
        :return bool: 是否收藏成功
        """
        # 加载记录
        record, _, is_avs_exists = self.check_has_record()
        if not record:
            record, avs = {}, []
        else:
            if not is_avs_exists:
                avs = []
            else:
                avs = record["avs"]
        # 检查记录是否存在
        for av in avs:
            if av["id"].lower() == id.lower():
                return True
        # 如果记录需要更新则写回记录
        avs.append({"id": id.lower(), "stars": stars})
        record["avs"] = avs
        return self.renew_record(record)

    def undo_record_star_by_id(self, star_id: str) -> bool:
        """取消收藏演员

        :param str star_id: 演员id
        :return bool: 是否取消收藏成功
        """
        # 加载记录
        record, exists, _ = self.check_has_record()
        if not record or not exists:
            return False
        stars = record["stars"]
        exists = False
        # 删除记录
        for i, star in enumerate(stars):
            if star["id"].lower() == star_id.lower():
                del stars[i]
                exists = True
                break
        # 更新记录
        if exists:
            record["stars"] = stars
            return self.renew_record(record)
        return True

    def undo_record_id(self, id: str) -> bool:
        """取消收藏番号

        :param str id: 番号
        :return bool: 是否取消收藏成功
        """
        # 加载记录
        record, _, exists = self.check_has_record()
        if not record or not exists:
            return False
        avs = record["avs"]
        exists = False
        # 删除记录
        for i, av in enumerate(avs):
            if av["id"].lower() == id.lower():
                del avs[i]
                exists = True
                break
        # 更新记录
        if exists:
            record["avs"] = avs
            return self.renew_record(record)
        return True


class BotCacheDb:
    CACHE_AV = {
        "prefix": "av-",
        "expire": 3600 * 24 * 30,
    }
    CACHE_STAR = {
        "prefix": "star-",
        "expire": 0,  # 永不过期
    }
    CACHE_RANK = {
        "prefix": "rank-",
        "expire": 3600 * 24 * 7,
    }
    CACHE_SAMPLE = {
        "prefix": "sample-",
        "expire": 3600 * 24 * 30,
    }
    CACHE_MAGNET = {
        "prefix": "magnet-",
        "expire": 3600 * 24 * 5,
    }
    CACHE_PV = {
        "prefix": "pv-",
        "expire": 3600 * 24 * 15,
    }
    CACHE_FV = {
        "prefix": "fv-",
        "expire": 3600 * 24 * 15,
    }
    CACHE_STARS_MSG = {
        "prefix": "stars-msg-",
        "expire": 3600 * 24 * 5,
    }
    CACHE_COMMENT = {"prefix": "comment-", "expire": 3600 * 24 * 30}
    CACHE_NICE_AVS_OF_STAR = {
        "prefix": "nice-avs-of-star-",
        "expire": 3600 * 24 * 15,
    }
    CACHE_JLIB_PAGE_NICE_AVS = {
        "prefix": "jlib-page-nice-avs-",
        "expire": 3600 * 24 * 7,
    }
    CACHE_JLIB_PAGE_NEW_AVS = {
        "prefix": "jlib-page-new-avs-",
        "expire": 3600 * 24 * 2,
    }
    CACHE_STAR_JA_NAME = {"prefix": "star-ja-name-", "expire": 3600 * 24 * 30 * 6}
    CACHE_NEW_AVS_OF_STAR = {
        "prefix": "new-avs-of-star-",
        "expire": 3600 * 24 * 12,
    }

    TYPE_AV = 1
    TYPE_STAR = 2
    TYPE_RANK = 3
    TYPE_SAMPLE = 4
    TYPE_MAGNET = 5
    TYPE_PV = 6
    TYPE_FV = 7
    TYPE_STARS_MSG = 8
    TYPE_COMMENT = 10
    TYPE_NICE_AVS_OF_STAR = 11
    TYPE_JLIB_PAGE_NICE_AVS = 12
    TYPE_JLIB_PAGE_NEW_AVS = 13
    TYPE_STAR_JA_NAME = 14
    TYPE_NEW_AVS_OF_STAR = 16

    TYPE_MAP = {
        TYPE_AV: CACHE_AV,
        TYPE_STAR: CACHE_STAR,
        TYPE_RANK: CACHE_RANK,
        TYPE_SAMPLE: CACHE_SAMPLE,
        TYPE_MAGNET: CACHE_MAGNET,
        TYPE_PV: CACHE_PV,
        TYPE_FV: CACHE_FV,
        TYPE_STARS_MSG: CACHE_STARS_MSG,
        TYPE_COMMENT: CACHE_COMMENT,
        TYPE_NICE_AVS_OF_STAR: CACHE_NICE_AVS_OF_STAR,
        TYPE_JLIB_PAGE_NICE_AVS: CACHE_JLIB_PAGE_NICE_AVS,
        TYPE_JLIB_PAGE_NEW_AVS: CACHE_JLIB_PAGE_NEW_AVS,
        TYPE_STAR_JA_NAME: CACHE_STAR_JA_NAME,
        TYPE_NEW_AVS_OF_STAR: CACHE_NEW_AVS_OF_STAR,
    }

    def __init__(self, host: str, port: int, use_cache: str):
        """初始化

        :param str host: redis host
        :param int port: redis port
        :param str use_cache: 是否使用缓存 '1' | '0'
        """
        self.use_cache = use_cache == "1"
        if not self.use_cache:
            return
        try:
            self.redis = redis.StrictRedis(
                host=host, port=port, decode_responses=True, db=0
            )
            self.redis.ping()
            LOG.info("连接到 Redis 缓存")
        except Exception as e:
            LOG.error(f"连接 Redis 失败: {e}, 缓存功能已禁用")
            self.use_cache = False

    def remove_cache(self, key: str, type: int):
        if not self.use_cache:
            return
        try:
            cache_type = self.TYPE_MAP[type]
            self.redis.delete(f"{cache_type['prefix']}{key}")
        except Exception as e:
            LOG.error(f"移除 Redis 缓存失败: key={key}, type={type}, error={e}")

    def set_cache(self, key: str, value, type: int, expire=None):
        if not self.use_cache:
            return
        try:
            cache_type = self.TYPE_MAP[type]
            cache_key = f"{cache_type['prefix']}{key}"
            cache_value = json.dumps(value)
            
            ex = expire if expire is not None else cache_type["expire"]
            if ex > 0:
                self.redis.setex(cache_key, ex, cache_value)
            else:
                self.redis.set(cache_key, cache_value)
        except Exception as e:
            LOG.error(f"设置 Redis 缓存失败: key={key}, type={type}, error={e}")

    def get_cache(self, key, type: int) -> any:
        if not self.use_cache:
            return None
        try:
            cache_type = self.TYPE_MAP[type]
            cache_key = f"{cache_type['prefix']}{key}"
            value = self.redis.get(cache_key)
            return json.loads(value) if value else None
        except Exception as e:
            LOG.error(f"获取 Redis 缓存失败: key={key}, type={type}, error={e}")
            return None
