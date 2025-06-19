import logging
from logic import run_logic

import azure.functions as func

def main(youtubeCrawlingTimer: func.TimerRequest) -> None:
    logging.info("Run Scheduler!")
    run_logic()
    logging.info("Scheduler Complete!")