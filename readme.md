# 项目依赖安装
```shell
pip install -r requirements.txt
```

# 运行方式
```shell
python app.py --flask
```

# 注意事项
本搜种器主要用于本人星露谷挑战档，一切设计思路和用途都是针对本档写的，还没有泛用化，还没有做图形交互界面，只写了旧随机还没有写新随机

不会用可以在这个视频下面留言，我帮你搜：https://www.bilibili.com/video/BV1FRYYzhEeS

未来有空会再productionalize

---

# 设计思路
第一，我想预测天气（weather），我希望知道在春季（spring）和夏季（summer）每一天的天气

第二，我想预测沙漠节（desert festival）的商人（vendor），有一些村民（villager）会随机来沙漠节出售物品，每天会有两个人，我想知道是哪两个人会来出售

第三，我想知道矿井混合宝箱（remixed rewards in mine chests）的内容

第四，我想预测春5（spring 5），也就是游戏第五天里，矿井（mines）的怪物层（Monster and slime infestations），也就是有一些层数有可能会变成怪物层，我想知道是哪几层

第五，我想预测春1（spring 1）和春2（spring 2），也就是游戏的第一天和第二天，星之果实餐吧（stardrop saloon）的垃圾桶（garbag can）里是否产生物品

---

# 正式

运行方式：python app.py

所有参数在app.py中修改

使用ENABLE_FILTER可以开启/关闭筛选功能

种子筛选范围：SEED_START / SEED_END

## 功能一：天气预测（已完成）
填写参数WEATHER_CLAUSES

提供起始、结束日期（含）：start / end

需要预测的天气类型：targets

最少天数：min_count

例如：春1-春28，至少10个雨天

多个条件可以同时要求


## 功能二：矿井怪物层预测（已完成）
提供起始、结束日期（含）：MINES_START_DAY / MINES_END_DAY

起始、结束层数（含）：FLOOR_START / FLOOR_END

可以筛掉有怪物层的种子

例：春5，要求1-90层没有怪物层

## 功能三：矿井混合宝箱（已完成）
提供筛选条件：CHEST_RULES

例：要求20层是磁铁戒指，且80是长柄锤或110是巨锤

```CHEST_RULES_MODE = "ALL"  # "ALL" 或 "ANY"
CHEST_RULES: List[ChestRule] = [
    # 示例：20层=磁铁戒指 且 (80层=长柄锤 或 110层=巨锤)
    (20, "磁铁戒指"),
    [(80, "长柄锤"), (110, "巨锤")],
]
```
可以嵌套要求，例：20层出磁铁戒指 并且 （（80层出长柄锤且110层出太空之靴）或者（80层出蹈火者靴且110层出巨锤））
```CHEST_RULES: List[ChestRule] = [
    (20, "磁铁戒指"),
    [   # 这是一个 OR 组
        [ (80, "长柄锤"),   (110, "太空之靴") ],  # AND 子组 A
        [ (80, "蹈火者靴"), (110, "巨锤") ],      # AND 子组 B
    ],
]
```

## 功能四：沙漠节摆摊（已完成）
判断莉亚（出售100硬木）且/或贾斯（出售魔法糖冰棍）是否来摆摊

提供筛选参数：REQUIRE_LEAH / REQUIRE_JAS 

研究发现，前面天数晚上睡觉的时间会导致存档时npc位置不同，影响后续npc列表和沙漠节商人选择。目前默认以凌晨2点睡觉的序列预测贾斯。

贾斯有待double check，但莉亚应该是准的


## 功能五：垃圾桶（已完成）
提供起始、结束日期（含）：saloon_start_day / saloon_end_day

在日期范围内，酒吧垃圾桶至少一次出现每日菜品

## 功能六：仙子（已完成）

春1晚上出现仙子

可以搜其他日期：NIGHT_CHECK_DAY
