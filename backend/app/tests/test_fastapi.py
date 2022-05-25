import pytest
from dramatiq import Worker
from fastapi.testclient import TestClient

import app.tasks as tasks
from app.dramatiq import DRAMATIQ_BROKER
from app.hashids import hashids_
from app.main import app
from app.tests.test_database import init_and_destroy_db  # noqa

client = TestClient(app)


@pytest.fixture()
def stub_broker():
    DRAMATIQ_BROKER.flush_all()
    return DRAMATIQ_BROKER


@pytest.fixture()
def stub_worker():
    worker = Worker(DRAMATIQ_BROKER, worker_timeout=100)
    worker.start()
    yield worker
    worker.stop()


def test_get_now():
    response = client.get("/now")
    assert response.status_code == 200


def test_process_text(init_and_destroy_db):  # noqa
    response = client.get("/history")
    assert response.status_code == 200
    print(response.json())

    response = client.get("/stats")
    assert response.status_code == 200
    print(response.json())

    response = client.post(
        "/process_text",
        json={
            "text": "Состояние удовлетворительное.  РОСТ= 174см,   ВЕС=100 кг,  ИМТ=33,03.  Ожирение 1  ст.  Тоны сердца  приглушены  аритмичные, мерцательная аритмия  с  ЧСС=86   уд/мин.  АД= 127/103  мм.рт.ст.  В легких дыхание везикулярное,хрипов нет.  Живот   увеличен в обьеме  за счет п/к жирового слоя.  Отеков нет.  По ЭКГ фибрилляция предсердий с ЧСС=62-74уд. мин. Диффузные изменения миокарда.  Хс=   нет данных.  ХМ ЭКГ и заключение их НИИПК прилагаются.",  # noqa
            "type": "all",
        },
    )
    assert response.status_code == 202
    data = response.json()
    run_id = data["run_id"]

    response = client.get(f"/run/{run_id}")
    assert response.status_code == 202

    tasks.process_run(hashids_.from_hash_id(run_id))

    response = client.get(f"/run/{run_id}")
    assert response.status_code == 200

    response = client.get("/history")
    assert response.status_code == 200
    print(response.json())

    response = client.get("/stats")
    assert response.status_code == 200
    print(response.json())
