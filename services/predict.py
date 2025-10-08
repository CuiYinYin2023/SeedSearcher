from typing import List, Dict, Tuple, Optional, Union, Set
from functions.weather import WeatherPredictor, DayWeather
from functions.mines import MinesPredictor, DayInfested
from functions.chests import ChestsPredictor
from functions.trashcans import predict_saloon_trash_in_range

# -------- 天气 --------
def evaluate_weather_clauses(
    wp: WeatherPredictor,
    clauses: List[Dict],
    default_targets: Tuple[str, ...]
) -> Tuple[bool, List[DayWeather]]:
    if not clauses:
        return True, []

    mn = min(int(c["start"]) for c in clauses)
    mx = max(int(c["end"]) for c in clauses)
    all_days = wp.predict_range(mn, mx)
    by_day: Dict[int, DayWeather] = {d.abs_day: d for d in all_days}

    ok_all = True
    matched_union: Dict[int, DayWeather] = {}
    for c in clauses:
        s = int(c["start"]); e = int(c["end"]); need = int(c["min_count"])
        t = tuple(c.get("targets", default_targets))
        tset = set(t)
        hits = []
        for day in range(s, e + 1):
            dw = by_day.get(day)
            if dw and dw.weather_en in tset:
                hits.append(dw)
                matched_union[dw.abs_day] = dw
        if len(hits) < need:
            ok_all = False

    merged = [by_day[d] for d in sorted(matched_union.keys())]
    return ok_all, merged

# -------- 矿井 --------
def no_infested_in_range(mp: MinesPredictor, start_day: int, end_day: int, floor_start: int, floor_end: int) -> Tuple[bool, List[DayInfested]]:
    all_days = mp.predict_infested_in_range(start_day, end_day)
    ok = True
    for d in all_days:
        if any(floor_start <= f <= floor_end for f in d.floors):
            ok = False
            break
    return ok, all_days

# -------- 宝箱（嵌套 OR） --------
ChestAtom = Tuple[int, str]
ChestGroup = List[ChestAtom]
ChestRule = Union[ChestAtom, ChestGroup]

def collect_levels_from_rules(rules: List[ChestRule]) -> List[int]:
    levels: Set[int] = set()
    def walk(node):
        if isinstance(node, list):
            for x in node:
                walk(x)
        else:
            lv, _ = node
            levels.add(lv)
    for r in rules:
        walk(r)
    return sorted(levels)

def _normalize_rules(cp: ChestsPredictor, rules: List[ChestRule]) -> List[ChestRule]:
    def norm_node(node):
        if isinstance(node, list):
            return [norm_node(x) for x in node]
        else:
            lv, item = node
            return (lv, cp.normalize_item(item))
    return [norm_node(r) for r in rules]

def check_chest_rules_nested(cp: ChestsPredictor, rules: List[ChestRule], mode: str) -> Tuple[bool, Dict[int, Optional[str]]]:
    if not rules:
        return True, {}
    rules_norm = _normalize_rules(cp, rules)
    levels = collect_levels_from_rules(rules_norm)
    pred = cp.predict_levels(levels)

    def atom_ok(atom: ChestAtom) -> bool:
        lv, want = atom
        return pred.get(lv) == want

    def or_group_ok(group: List[Union[ChestAtom, List[ChestAtom]]]) -> bool:
        for elem in group:
            if isinstance(elem, list):
                if all(atom_ok(a) for a in elem):
                    return True
            else:
                if atom_ok(elem):
                    return True
        return False

    def eval_top(node) -> bool:
        if isinstance(node, list):
            return or_group_ok(node)
        else:
            return atom_ok(node)

    flags = [eval_top(n) for n in rules_norm]
    ok = any(flags) if mode.upper() == "ANY" else all(flags)
    return ok, pred

# -------- 酒吧垃圾桶（区间统计） --------
def evaluate_saloon_trash_range(
    seed: int,
    *,
    start_day: int,
    end_day: int,
    daily_luck: float = -0.1,
    has_garbage_book: bool = False,
    daily_luck_by_day: dict | None = None,
    require_min_hit_days: int = 1,
):
    out = predict_saloon_trash_in_range(
        seed,
        start_day,
        end_day,
        has_garbage_book=has_garbage_book,
        daily_luck=daily_luck,
        daily_luck_by_day=daily_luck_by_day,
    )
    results = out["results"]
    days_total = out["summary"]["days_total"]
    dish_days = [d for d in range(start_day, end_day + 1) if results[d].source == "DishOfTheDay"]
    dish_days_hit = len(dish_days)
    ok = dish_days_hit >= max(1, int(require_min_hit_days))
    if dish_days:
        hit_str = ",".join(str(d) for d in dish_days)
        tag = f"酒吧垃圾桶（Dish）命中 {dish_days_hit}/{days_total} 天（{hit_str}）"
    else:
        tag = f"酒吧垃圾桶（Dish）命中 0/{days_total} 天"
    out_ext = {
        "results": results,
        "summary": {
            **out["summary"],
            "dish_days": dish_days,
            "dish_days_hit": dish_days_hit,
            "require_min_hit_days": int(require_min_hit_days),
        }
    }
    return ok, tag, out_ext
