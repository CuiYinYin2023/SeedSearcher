from typing import List, Dict, Tuple, Union, Optional

# ========== 功能总开关 ==========
ENABLE_WEATHER_FILTER = False  # 天气
ENABLE_MINES_FILTER   = False  # 矿井怪物层
ENABLE_CHESTS_FILTER  = True   # 混合宝箱筛选（保持你之前的默认）
ENABLE_DESERT_FILTER  = False  # 沙漠节
ENABLE_SALOON_FILTER  = False  # 酒吧垃圾桶
ENABLE_NIGHT_EVENT_FILTER = False   # 夜间事件（仙子）
# =================================

# ========= 种子范围 =========
SEED_START = 0      # 从这里开始
SEED_RANGE = 500    # 共筛这么多个

# ========= 天气筛选参数（多区间规则）=========
TARGET_TYPES: Tuple[str, ...] = ("Rain", "Storm", "Green Rain")  # 默认雨天类型集合

# 每条规则：start, end, min_count, 可选 targets（不写则用上面的 TARGET_TYPES）
WEATHER_CLAUSES: List[Dict] = [
    {"start": 7,  "end": 7,  "min_count": 1},
    {"start": 14, "end": 26, "min_count": 4},
    {"start": 30, "end": 27, "min_count": 10},
]

# ========= 矿井筛选参数 =========
MINES_START_DAY = 5     # 绝对天数
MINES_END_DAY   = 5
FLOOR_START     = 1
FLOOR_END       = 85
REQUIRE_NO_INFESTED = True  # True=要求“完全没有怪物/史莱姆层”

# ========= 混合宝箱筛选参数（支持嵌套 OR）=========
from typing import List as _List, Tuple as _Tuple, Union as _Union
ChestAtom = _Tuple[int, str]
ChestGroup = _List[ChestAtom]             # OR 组
ChestRule = _Union[ChestAtom, ChestGroup] # 顶层元素：单条 或 OR 组

CHEST_RULES_MODE = "ALL"
CHEST_RULES: _List[ChestRule] = [
    (20, "磁铁戒指"),
    [   # 这是一个 OR 组
        [ (80, "长柄锤"),   (110, "太空之靴") ],  # AND 子组 A
        [ (80, "蹈火者靴"), (110, "巨锤") ],      # AND 子组 B
    ],
]

# ========= 沙漠节筛选参数 =========
REQUIRE_LEAH = True  # 至少一天出现 Leah
REQUIRE_JAS  = True  # 至少一天出现 Jas

# ===== Saloon 垃圾桶（日期区间） =====
saloon_start_day = 1               # 开始日期（春1 = 1）
saloon_end_day = 2                 # 结束日期
saloon_daily_luck = -0.1           # 统一运势（或使用 daily_luck_by_day 覆盖）
saloon_has_book = False            # 是否读过垃圾之书
saloon_require_min_hit = 1         # 至少命中 N 天才算通过

# ===== 夜间事件 =====
NIGHT_CHECK_DAY = 1                # 检查“春1”的夜间事件
NIGHT_GREENHOUSE_UNLOCKED = False  # 温室已修复？只影响风暴提示，不影响仙子判定

# 其他参数
USE_LEGACY   = True
SHOW_DATES   = True
PROCESSES    = 0
CHUNKSIZE    = 1000

__all__ = [
    # switches
    'ENABLE_WEATHER_FILTER','ENABLE_MINES_FILTER','ENABLE_CHESTS_FILTER','ENABLE_DESERT_FILTER','ENABLE_SALOON_FILTER','ENABLE_NIGHT_EVENT_FILTER',
    # ranges
    'SEED_START','SEED_RANGE',
    # weather
    'TARGET_TYPES','WEATHER_CLAUSES',
    # mines
    'MINES_START_DAY','MINES_END_DAY','FLOOR_START','FLOOR_END','REQUIRE_NO_INFESTED',
    # chests
    'ChestAtom','ChestGroup','ChestRule','CHEST_RULES_MODE','CHEST_RULES',
    # desert
    'REQUIRE_LEAH','REQUIRE_JAS',
    # saloon
    'saloon_start_day','saloon_end_day','saloon_daily_luck','saloon_has_book','saloon_require_min_hit',
    # night
    'NIGHT_CHECK_DAY','NIGHT_GREENHOUSE_UNLOCKED',
    # misc
    'USE_LEGACY','SHOW_DATES','PROCESSES','CHUNKSIZE'
]
