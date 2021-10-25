from time import sleep

from sqlmodel import select

from icon_governance.config import settings
from icon_governance.db import session
from icon_governance.log import logger
from icon_governance.models.preps import Prep
from icon_governance.utils.rpc import (
    convert_hex_int,
    getDelegation,
    getPReps,
    post_rpc_json,
)


def prep_attributes_cron():

    while True:
        logger.info("")
        preps = post_rpc_json(getPReps())
        if preps is None:
            logger.info("No preps found from rpc. Chilling for a bit.")
            sleep(60)
            continue

        for p in preps["preps"]:
            prep = session.get(Prep, p["address"])
            if prep is None:
                logger.info("No preps found in db? Should not ever happen cuz of db_init.")
                continue

            delegation = post_rpc_json(getDelegation(p["address"]))

            prep.voted = convert_hex_int(delegation["totalDelegated"]) / 1e18
            prep.voting_power = convert_hex_int(delegation["votingPower"]) / 1e18

            prep.total_blocks = convert_hex_int(p["totalBlocks"])
            prep.total_blocks = convert_hex_int(p["validatedBlocks"])
            prep.total_blocks = convert_hex_int(p["unvalidatedSequenceBlocks"])

            prep.delegated = convert_hex_int(p["delegated"]) / 1e18
            prep.stake = convert_hex_int(p["stake"]) / 1e18
            prep.irep = convert_hex_int(p["irep"]) / 1e18

            prep.grade = p["grade"]
            prep.penalty = p["penalty"]

            session.add(prep)
            session.commit()

        logger.info("Prep attributes ran.")
        sleep(settings.CRON_SLEEP_SEC)


if __name__ == "__main__":
    prep_attributes_cron()