from abc import ABC
import os
from time import sleep
from typing import Callable, Dict, List
from faker import Faker
from loguru import logger
import requests
from random import SystemRandom

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://backend:8000")
# API_URL = os.getenv("API_URL", "http://localhost:8000")

AVAILABLE_ENDPOINTS = [
    "stats",
    "history",
    "process_text",
]

rnd = SystemRandom()

faker = Faker("ru_RU")


def get_text_to_process() -> Dict[str, str]:
    text = ""
    type_ = "acute_coronary_syndrome"

    if rnd.randint(0, 1):
        temperature_base = 34
        temperature_addition = 5

        temperature = temperature_base + temperature_addition * rnd.random()

        pressure_base = 60
        pressure = pressure_base + rnd.randint(0, 30)
        text = (
            f"Температура {temperature:.1f}."
            f"Давление высокое - {pressure + 40} на {pressure}."
        )
    else:
        text = faker.text(max_nb_chars=60)

    return {"text": text, "type": type_}


class Endpoint(ABC):
    def request(self) -> None:
        raise NotImplementedError


class GetEndpoint:
    def __init__(self, path: str) -> None:
        self.url = API_URL + path

    def request(self) -> None:
        logger.debug(f"Requesting {self.url}")
        response = requests.get(self.url, timeout=15)
        logger.debug(f"Got status code {response.status_code}")


class PostEndpoint:
    def __init__(self, path: str, data_function: Callable) -> None:
        self.url = API_URL + path
        self.data_function = data_function

    def request(self) -> None:
        data = self.data_function()
        logger.debug(f"Requesting {self.url} with data: {data}")
        response = requests.post(self.url, json=data, timeout=15)
        logger.debug(f"Got status code {response.status_code}")


class Simulator:
    def __init__(self, sleep_base: float = 2.0) -> None:
        history_endpoint = GetEndpoint("/history")
        stats_endpoint = GetEndpoint("/stats")
        process_text_endpoint = PostEndpoint(
            "/process_text", get_text_to_process
        )

        self.endpoints: List[Endpoint] = [
            history_endpoint,
            stats_endpoint,
            process_text_endpoint,
        ]
        self.sleep_base = sleep_base

    def start(self):
        logger.info("Start simulating activity ...")

        try:
            self._start()
        except KeyboardInterrupt:
            logger.info("Shutting down ...")

    def _start(self):
        while True:
            endpoint_index = rnd.randint(0, 2)
            endpoint = self.endpoints[endpoint_index]
            endpoint.request()
            sleeping_for = rnd.random() * self.sleep_base
            logger.info(f"Sleeping for {sleeping_for:.2f} seconds ...")
            sleep(sleeping_for)


if __name__ == "__main__":
    simulator = Simulator()
    simulator.start()
