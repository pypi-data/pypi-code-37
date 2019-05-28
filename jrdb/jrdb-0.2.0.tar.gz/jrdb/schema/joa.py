schema = {
    "name": "joa",
    "type": "record",
    "fields": [
        {"start":   0, "end":   2, "type": "string", "name": "place_id"},
        {"start":   2, "end":   4, "type": "string", "name": "year"},
        {"start":   4, "end":   5, "type": "string", "name": "kai"},
        {"start":   5, "end":   6, "type": "string", "name": "nichi"},
        {"start":   6, "end":   8, "type": "string", "name": "number_of_race"},
        {"start":   8, "end":  10, "type": "string", "name": "pp"},
        {"start":  10, "end":  18, "type": "string", "name": "horse_id"},
        {"start":  18, "end":  54, "type": "string", "name": "horse_name"},
        {"start":  54, "end":  59, "type": "string", "name": "base_win_odds"},
        {"start":  59, "end":  64, "type": "string", "name": "base_show_odds"},
        {"start":  64, "end":  69, "type": "string", "name": "cid_training_raw_score"},
        {"start":  69, "end":  74, "type": "string", "name": "cid_stable_raw_score"},
        {"start":  74, "end":  79, "type": "string", "name": "cid_raw_score"},
        {"start":  79, "end":  82, "type": "string", "name": "cid"},
        {"start":  82, "end":  87, "type": "string", "name": "ls_score"},
        {"start":  87, "end":  88, "type": "string", "name": "ls_evaluation"},
        {"start":  88, "end":  89, "type": "string", "name": "em"},
        {"start":  89, "end":  90, "type": "string", "name": "stable_bb_mark"},
        {"start":  90, "end":  95, "type": "string", "name": "stable_bb_fav_win_roi"},
        {"start":  95, "end": 100, "type": "string", "name": "stable_bb_fav_place_rate"},
        {"start": 100, "end": 101, "type": "string", "name": "jockey_bb_mark"},
        {"start": 101, "end": 106, "type": "string", "name": "jockey_bb_fav_win_roi"},
        {"start": 106, "end": 111, "type": "string", "name": "jockey_bb_fav_place_rate"}
    ]
}
