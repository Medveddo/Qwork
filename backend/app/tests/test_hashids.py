from app.hashids import hashids_


def test_two_way_conversion():
    secret_id = 3
    hashid = hashids_.to_hash_id(secret_id)
    print(f"{secret_id} -> {hashid}")
    assert secret_id == hashids_.from_hash_id(hashid)
