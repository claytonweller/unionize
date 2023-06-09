from modules.worker.data_class import Worker


def find_matching_union_worker(union_workers: list[Worker], potential_worker: Worker):
    def check(worker):
        # TODO eventually we'll do an email match as well but that's not in POC scope
        phone_match = potential_worker['encodedPhone'] == worker['encodedPhone']
        return phone_match

    matches = filter(check, union_workers)
    match = next(matches, None)
    print(f'MATCH - {match}')
    return match
