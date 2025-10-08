from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import time
from functools import partial
from typing import Iterable, Tuple, List, Dict, Optional, Union, Set
from utils.scan_engine import run_scan
from functions.weather import WeatherPredictor, DayWeather
from functions.mines import MinesPredictor, DayInfested
from functions.chests import ChestsPredictor
from functions.desert_festival import DesertFestivalPredictor
from functions.trashcans import predict_saloon_trash_in_range
from functions.night_events import predict_night_event_for_day
from config import (
    ENABLE_WEATHER_FILTER, ENABLE_MINES_FILTER, ENABLE_CHESTS_FILTER, ENABLE_DESERT_FILTER,
    ENABLE_SALOON_FILTER, ENABLE_NIGHT_EVENT_FILTER,
    SEED_START, SEED_RANGE,
    TARGET_TYPES, WEATHER_CLAUSES,
    MINES_START_DAY, MINES_END_DAY, FLOOR_START, FLOOR_END, REQUIRE_NO_INFESTED,
    ChestAtom, ChestGroup, ChestRule, CHEST_RULES_MODE, CHEST_RULES,
    REQUIRE_LEAH, REQUIRE_JAS,
    saloon_start_day, saloon_end_day, saloon_daily_luck, saloon_has_book, saloon_require_min_hit,
    NIGHT_CHECK_DAY, NIGHT_GREENHOUSE_UNLOCKED,
    USE_LEGACY, SHOW_DATES, PROCESSES, CHUNKSIZE,
)
from api.routes import bp as api_bp
from services.predict import (
    evaluate_weather_clauses,
    no_infested_in_range,
    collect_levels_from_rules,
    check_chest_rules_nested,
    evaluate_saloon_trash_range,
)


dist_path = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')
app = Flask(__name__, static_folder=dist_path, template_folder=dist_path)

# 启用 CORS（仅开放 /api/* 路径），允许本地开发端口访问
_allowed_origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]
CORS(
    app,
    resources={r"/api/*": {"origins": _allowed_origins}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "access-token"],
)

# 首页和静态资源
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    file_path = os.path.join(app.static_folder, path)
    if path != "" and os.path.exists(file_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# 注册 API 蓝图
app.register_blueprint(api_bp)

## 上述配置、常量已移动到 config.py

## ---------- helpers（部分工具函数已移至 services.predict） ----------

def fmt_weather(days: List[DayWeather]) -> str:
    return "、".join([f"{d.season_en}{d.dom}({d.weather_zh})" for d in days])

def fmt_mines(details: List[DayInfested], floor_start: int, floor_end: int) -> str:
    parts = []
    for d in details:
        bad = sorted([f for f in d.floors if floor_start <= f <= floor_end])
        if bad:
            parts.append(f"Day{d.abs_day}: {bad}")
    return " | ".join(parts) if parts else "无"

# ====== 宝箱（支持嵌套 OR）的工具函数 ======

def fmt_chests_human(cp: ChestsPredictor, details: Dict[int, Optional[str]]) -> str:
    pairs = []
    for lv in sorted(details.keys()):
        can = details[lv]
        if can is None:
            name = "（非宝箱层）"
        else:
            name = cp.display_name(can)
        pairs.append(f"L{lv}={name}")
    return ", ".join(pairs) if pairs else "无规则"

## evaluate_weather_clauses / no_infested_in_range / check_chest_rules_nested /
## collect_levels_from_rules / evaluate_saloon_trash_range 已从 services.predict 引入


# ---------- 顶层 worker ----------
def worker(
    seed: int,
    # weather
    enable_weather: bool, weather_clauses: List[Dict], targets: Tuple[str, ...], use_legacy: bool,
    # mines
    enable_mines: bool, mines_start: int, mines_end: int, floor_start: int, floor_end: int, require_no_infested: bool,
    # chests
    enable_chests: bool, chest_rules_mode: str, chest_rules: List[ChestRule],
    # desert festival
    enable_desert: bool, require_leah: bool, require_jas: bool,
):
    """
    动态估价 + 短路：
      - 将启用的功能封装为任务，估算成本并排序
      - 按成本从小到大执行；任一项失败立即返回
    返回结构保持不变。
    """
    # 默认返回容器（短路时也能返回）
    matched: List[DayWeather] = []
    mines_detail: List[DayInfested] = []
    chests_detail: Dict[int, Optional[str]] = {}
    desert_detail: Dict[str, List[str]] = {}
    saloon_out = None
    saloon_tag = None
    saloon_ok = True
    night_detail = None
    night_ok = True

    tasks = []  # (name, cost_estimate, fn)

    # 夜间事件
    if ENABLE_NIGHT_EVENT_FILTER:
        cost_night = 1
        def _eval_night():
            nonlocal night_detail, night_ok
            ne = predict_night_event_for_day(
                seed,
                NIGHT_CHECK_DAY,
                day_adjust=0,
                greenhouse_unlocked=NIGHT_GREENHOUSE_UNLOCKED,
            )
            night_detail = ne
            night_ok = ne.is_fairy
            return night_ok
        tasks.append(("night", cost_night, _eval_night))

    # 沙漠节
    if enable_desert:
        cost_desert = 3  # 固定 3 天
        def _eval_desert():
            nonlocal desert_detail
            ok = True
            df = DesertFestivalPredictor(
                game_id=seed,
                use_legacy=use_legacy,
                year=1,
                leo_moved=False,
                debug=False
            )
            res = df.vendors_for_three_days()
            v15, v16, v17 = res[0], res[1], res[2]
            desert_detail = {"春15": v15, "春16": v16, "春17": v17}
            has_leah = any("Leah" in vendors for vendors in (v15, v16, v17))
            has_jas  = any("Jas"  in vendors for vendors in (v15, v16, v17))
            if require_leah and not has_leah:
                ok = False
            if require_jas and not has_jas:
                ok = False
            return ok
        tasks.append(("desert", cost_desert, _eval_desert))

    # 宝箱
    if enable_chests:
        unique_levels = len(collect_levels_from_rules(chest_rules))
        cost_chests = max(1, unique_levels)
        def _eval_chests():
            nonlocal chests_detail
            cp = ChestsPredictor(game_id=seed, use_legacy=use_legacy)
            ok, detail = check_chest_rules_nested(cp, chest_rules, chest_rules_mode)
            chests_detail = detail
            return ok
        tasks.append(("chests", cost_chests, _eval_chests))

    # 天气（多区间 AND）
    if enable_weather:
        # 估算成本：所有子区间长度之和（更贴近实际）
        cost_weather = max(1, sum(int(c["end"]) - int(c["start"]) + 1 for c in weather_clauses))
        def _eval_weather():
            nonlocal matched
            wp = WeatherPredictor(game_id=seed, use_legacy=use_legacy)
            ok, matched_days = evaluate_weather_clauses(wp, weather_clauses, targets)
            matched = matched_days
            return ok
        tasks.append(("weather", cost_weather, _eval_weather))

    # 垃圾桶
    if ENABLE_SALOON_FILTER:
        span_saloon = max(0, saloon_end_day - saloon_start_day + 1)
        cost_saloon = max(1, span_saloon * 220)  # 经验系数
        def _eval_saloon():
            nonlocal saloon_out, saloon_tag, saloon_ok
            saloon_ok, saloon_tag, saloon_out = evaluate_saloon_trash_range(
                seed,
                start_day=saloon_start_day,
                end_day=saloon_end_day,
                daily_luck=saloon_daily_luck,
                has_garbage_book=saloon_has_book,
                daily_luck_by_day=None,
                require_min_hit_days=saloon_require_min_hit,
            )
            return saloon_ok
        tasks.append(("saloon", cost_saloon, _eval_saloon))

    # 矿井
    if enable_mines:
        span_mines = max(0, mines_end - mines_start + 1)
        cost_mines = max(1, span_mines * 1000)  # 经验系数（相对最贵）
        def _eval_mines():
            nonlocal mines_detail
            mp = MinesPredictor(game_id=seed, use_legacy=use_legacy)
            if require_no_infested:
                ok, mines_detail_local = no_infested_in_range(mp, mines_start, mines_end, floor_start, floor_end)
                mines_detail = mines_detail_local
                return ok
            else:
                mines_detail = mp.predict_infested_in_range(mines_start, mines_end)
                return True
        tasks.append(("mines", cost_mines, _eval_mines))

    # 没开任何功能 → 直接通过
    if not tasks:
        ok = True
        return seed, matched, mines_detail, chests_detail, desert_detail, ok, saloon_out, saloon_tag, saloon_ok, night_detail, night_ok

    # 动态排序 + 短路
    tasks.sort(key=lambda x: x[1])
    for _name, _cost, fn in tasks:
        if not fn():
            ok = False
            return seed, matched, mines_detail, chests_detail, desert_detail, ok, saloon_out, saloon_tag, saloon_ok, night_detail, night_ok

    # 全部通过
    ok = True
    return seed, matched, mines_detail, chests_detail, desert_detail, ok, saloon_out, saloon_tag, saloon_ok, night_detail, night_ok


# ---------- main ----------
def main():
    seeds: Iterable[int] = range(SEED_START, SEED_START + SEED_RANGE + 1)
    processes = None if PROCESSES == 0 else PROCESSES

    mp_worker = partial(
        worker,
        enable_weather=ENABLE_WEATHER_FILTER,
        weather_clauses=WEATHER_CLAUSES,
        targets=TARGET_TYPES,
        use_legacy=USE_LEGACY,
        enable_mines=ENABLE_MINES_FILTER,
        mines_start=MINES_START_DAY,
        mines_end=MINES_END_DAY,
        floor_start=FLOOR_START,
        floor_end=FLOOR_END,
        require_no_infested=REQUIRE_NO_INFESTED,
        enable_chests=ENABLE_CHESTS_FILTER,
        chest_rules_mode=CHEST_RULES_MODE,
        chest_rules=CHEST_RULES,
        enable_desert=ENABLE_DESERT_FILTER,
        require_leah=REQUIRE_LEAH,
        require_jas=REQUIRE_JAS,
    )

    t0 = time.time()
    results = run_scan(seeds, mp_worker, processes=processes, chunksize=CHUNKSIZE)
    elapsed = time.time() - t0

    hits = []
    for seed, matched, mines_detail, chests_detail, desert_detail, ok, saloon_out, saloon_tag, saloon_ok, night_detail, night_ok in results:
        if ok:
            hits.append(seed)
            print(f"命中种子 {seed}：", end="")
            tags = []
            if ENABLE_WEATHER_FILTER:
                tags.append(f"天气命中 {len(matched)} 天")
            if ENABLE_MINES_FILTER:
                if REQUIRE_NO_INFESTED:
                    tags.append(f"矿井[{MINES_START_DAY}-{MINES_END_DAY}]楼层[{FLOOR_START}-{FLOOR_END}]无怪物层")
                else:
                    tags.append("矿井筛选未启用或仅展示")
            if ENABLE_CHESTS_FILTER:
                tags.append("宝箱规则满足")
            if ENABLE_DESERT_FILTER:
                tags.append("沙漠节命中")
            if ENABLE_SALOON_FILTER and saloon_tag:
                tags.append(saloon_tag)
            if ENABLE_NIGHT_EVENT_FILTER and night_ok:
                tags.append(f"春{NIGHT_CHECK_DAY}夜=Fairy")

            print("；".join(tags) if tags else "（未启用任何筛选）")

            if SHOW_DATES:
                if ENABLE_WEATHER_FILTER:
                    print("  天气日期：", fmt_weather(matched) or "无")
                if ENABLE_MINES_FILTER and REQUIRE_NO_INFESTED:
                    print("  矿井异常：", fmt_mines(mines_detail, FLOOR_START, FLOOR_END))
                if ENABLE_CHESTS_FILTER:
                    cp_tmp = ChestsPredictor(game_id=seed, use_legacy=USE_LEGACY)
                    print("  宝箱掉落：", fmt_chests_human(cp_tmp, chests_detail))
                if ENABLE_DESERT_FILTER and desert_detail:
                    ds = " | ".join([f"{k}: {v}" for k, v in desert_detail.items()])
                    print("  沙漠节商人：", ds)
                if ENABLE_SALOON_FILTER and saloon_out:
                    s = saloon_out["summary"]
                    hit_days = s.get("dish_days", [])
                    hit_str = ",".join(map(str, hit_days)) if hit_days else "无"
                    print(f"  酒吧垃圾桶（Dish）：命中 {s.get('dish_days_hit', 0)}/{s['days_total']} 天；日期：{hit_str}")
                if ENABLE_NIGHT_EVENT_FILTER and night_detail is not None:
                    print(f"  夜间事件：春{NIGHT_CHECK_DAY}夜 -> {night_detail.event}")

    print(f"命中数量：{len(hits)}")
    if hits:
        print("前几个命中：", hits[:20])
    print(f"总耗时：{elapsed:.2f} 秒，进程数：{processes or 'auto'}，chunksize={CHUNKSIZE}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--flask":
        # 禁用 debug 模式以支持多进程
        app.run(debug=False, host='127.0.0.1', port=5000)
    else:
        main()
