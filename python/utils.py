def result_to_list(result):
    return [dict(u._mapping) for u in result.all()]