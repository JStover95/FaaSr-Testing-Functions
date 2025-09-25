from FaaSr_py.client.py_client_stubs import faasr_log, faasr_rank


def test_not_ranked() -> None:
    rank_info = faasr_rank()

    faasr_log(f"Rank info: {rank_info}")
    faasr_log(f"Rank: {rank_info.get('rank')}")
    faasr_log(f"Max rank: {rank_info.get('max_rank')}")
