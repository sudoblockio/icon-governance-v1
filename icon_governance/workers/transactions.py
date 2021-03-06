import json

from sqlmodel import select

from icon_governance.config import settings
from icon_governance.db import session_factory
from icon_governance.log import logger
from icon_governance.metrics import prom_metrics
from icon_governance.models.preps import Prep
from icon_governance.schemas.governance_prep_processed_pb2 import (
    GovernancePrepProcessed,
)
from icon_governance.utils.details import get_details
from icon_governance.workers.delegations import set_delegation
from icon_governance.workers.kafka import KafkaClient, get_current_offset
from icon_governance.workers.rewards import set_rewards


class TransactionsWorker(KafkaClient):
    msg_count: int = 0
    preps_created: int = 0
    preps_updated: int = 0

    def produce_prep(self, address, is_prep: bool = True):
        processes_prep = GovernancePrepProcessed(address=address, is_prep=is_prep)
        self.produce_protobuf(
            settings.PRODUCER_TOPIC_GOVERNANCE_PREPS,
            address,  # Keyed on address
            processes_prep,
        )

    def process(self, msg):
        # For backfilling only
        self.handle_backfill_stop(msg)

        # Filter on only txs to the governance address
        if settings.governance_address == msg.headers()[1][1]:
            return

        value = msg.value()

        # Ignore any unsuccessful txs
        if value.receipt_status != 1:
            return

        data = json.loads(value.data)

        address = value.from_address
        # timestamp = int(value.timestamp, 16) / 1e6

        # Ignore anything without a method call like contract creation events
        if data is not None:
            if "method" not in data:
                return
        else:
            return

        method = data["method"]

        # P-Reps
        if method in ["registerPRep", "setPrep", "unregisterPRep"]:

            try:
                params = data["params"]
            except KeyError:
                # Must be a failed Tx or something?
                logger.info(f"Skipping Tx - no params {value.hash}")
                return

            prep = self.session.get(Prep, address)

            if prep is not None:
                if method == "unregisterPRep":
                    logger.info(f"Prep unregistration tx hash {value.hash}")
                    prep.status = "unregistered"

                    # Emit message
                    self.produce_prep(value.from_address, is_prep=False)

                    self.preps_created += 1
                    prom_metrics.preps_created.set(self.preps_created)

                    self.session.add(prep)
                    self.session.commit()
                    return

                if prep.last_updated_block is not None:

                    if prep.last_updated_block > value.block_number and method == "setPrep":
                        logger.info(
                            f"Skipping setPrep call in tx_hash {value.hash} because it has since been updated."
                        )
                        return
            else:
                prep = Prep(
                    address=address,
                )

            if prep.last_updated_block is None:
                logger.info(f"Prep update registration tx hash {value.hash}")
                prep.created_block = value.block_number
                # prep.created_timestamp = timestamp

            prep.last_updated_block = value.block_number
            # prep.last_updated_timestamp = timestamp
            prep.name = params["name"]
            prep.email = params["email"]
            prep.city = params["city"]
            prep.website = params["website"]
            prep.country = params["country"]
            prep.details = params["details"]
            prep.p2p_endpoint = params["p2pEndpoint"]

            if "nodeAddress" in params:
                prep.node_address = params["nodeAddress"]

            details = get_details(params["details"])
            # Add information from details
            if details is not None:
                for k, v in details.items():
                    try:
                        setattr(prep, k, v)
                    except ValueError:
                        continue

            self.preps_updated += 1
            prom_metrics.preps_updated.set(self.preps_updated)

            self.session.add(prep)
            try:
                self.session.commit()
            except:
                self.session.rollback()
                raise

            # Emit message
            if method == "registerPRep":
                self.produce_prep(value.from_address)

        # Staking
        if method == "setStake":
            pass

        if method == "setDelegation":
            logger.info(f"set delegation {value.hash}")
            set_delegation(
                session=self.session,
                data=data,
                address=address,
                block_height=value.block_number,
                hash=value.hash,
            )

        if method == "claimIScore":
            logger.info(f"set delegation {value.hash}")
            set_rewards(session=self.session, value=value)

        if method == "registerProposal":
            pass

        if method == "cancelProposal":
            pass

        if method == "voteProposal":
            pass


def transactions_worker_head():
    with session_factory() as session:
        kafka = TransactionsWorker(
            session=session,
            topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
            consumer_group=settings.CONSUMER_GROUP + "-head",
        )

        kafka.start()


def transactions_worker_tail():

    with session_factory() as session:
        consumer_group, partition_dict = get_current_offset(session)

        kafka = TransactionsWorker(
            session=session,
            topic=settings.CONSUMER_TOPIC_TRANSACTIONS,
            consumer_group=consumer_group,
            partition_dict=partition_dict,
        )

        kafka.start()
