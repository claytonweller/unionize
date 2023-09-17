from modules.worker.data_class import Worker


def find_matching_union_worker(union_workers: list[Worker], phone: str, email: str) -> Worker | None:
    def check(worker: Worker):
        phone_match = phone == worker.phone
        email_match = email == worker.email
        # TODO since we're using the AWS sandbox right now we only have access to sending to one number
        # this should acutally be:
        # phone_match or email_match
        return phone_match and email_match

    matches = filter(check, union_workers)
    match = next(matches, None)
    print(f'MATCH - {match}')
    return match
