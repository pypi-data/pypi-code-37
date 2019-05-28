schema = {
    "name": "ukc",
    "type": "record",
    "fields": [
        {"start":   0, "end":   8, "type": "string", "name": "horse_id"},
        {"start":   8, "end":  44, "type": "string", "name": "horse_name"},
        {"start":  44, "end":  45, "type": "string", "name": "sex_id"},
        {"start":  45, "end":  47, "type": "string", "name": "coat_color_id"},
        {"start":  47, "end":  49, "type": "string", "name": "horse_mark_id"},
        {"start":  49, "end":  85, "type": "string", "name": "sire_name"},
        {"start":  85, "end": 121, "type": "string", "name": "dam_name"},
        {"start": 121, "end": 157, "type": "string", "name": "broodmare_sire_name"},
        {"start": 157, "end": 165, "type": "string", "name": "birthday"},
        {"start": 165, "end": 169, "type": "string", "name": "sire_birth_year"},
        {"start": 169, "end": 173, "type": "string", "name": "dam_birth_year"},
        {"start": 173, "end": 177, "type": "string", "name": "broodmare_sire_year"},
        {"start": 177, "end": 217, "type": "string", "name": "owner_name"},
        {"start": 217, "end": 219, "type": "string", "name": "owner_group_id"},
        {"start": 219, "end": 259, "type": "string", "name": "breeder_name"},
        {"start": 259, "end": 267, "type": "string", "name": "breeding_farm"},
        {"start": 267, "end": 268, "type": "string", "name": "deleted_flag"},
        {"start": 268, "end": 276, "type": "string", "name": "data_yyyymmdd"},
        {"start": 276, "end": 280, "type": "string", "name": "sire_kind_id"},
        {"start": 280, "end": 284, "type": "string", "name": "broodmare_sire_kind_id"}
    ]
}
