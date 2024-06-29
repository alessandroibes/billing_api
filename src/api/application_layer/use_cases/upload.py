import aioredis
import hashlib
import logging
import time

from api.app import get_redis_client
from api.application_layer.adapters.email_service import EmailService
from api.application_layer.adapters.boleto_service import BoletoService
from api.domain_layer.models.billing import Billing
from api.presentation_layer.utils import CsvFileException, Utils

logger = logging.getLogger("billing_api." + __name__)


class ProcessFileException(Exception):
    pass


class UploadUseCase():
    @classmethod
    async def process_file(cls, data: bytes):
        start_time = time.time()
        processed_items = 0

        try:
            redis = await get_redis_client()
            
            file_hash = hashlib.sha256(data).hexdigest()

            boletos_dict = Utils.read_csv(data)
            logger.info(f"boletos_dict: {boletos_dict}")

            number_of_boletos = len(boletos_dict)
            logger.info(f"Processing file received with {number_of_boletos} items.")

            processed_boletos = await redis.smembers(file_hash)
            set_of_processed_boletos = set(processed_boletos)

            number_of_processed_boletos = len(set_of_processed_boletos)
            if number_of_boletos == number_of_processed_boletos:
                logger.info("File already processed.")
                return
            
            pipe = redis.pipeline()
            for billing_data in boletos_dict:
                debt_id = billing_data['debtId']

                try:
                    if debt_id not in set_of_processed_boletos:
                        await Billing.process_billing(
                                billing_data=billing_data,
                                using_billing_service=BoletoService,
                                using_communication_service=EmailService
                            )
                        processed_items += 1
                        set_of_processed_boletos.add(debt_id)
                        pipe.sadd(file_hash, debt_id)
                except:
                    continue

            await pipe.execute()
        except CsvFileException as ex:
            logger.error(ex)
        except KeyError as ex:
            logger.error(f"Missing {ex}")
        except (
            aioredis.exceptions.ConnectionError,
            aioredis.exceptions.TimeoutError,
            aioredis.exceptions.AuthenticationError
        ) as ex:
            raise ProcessFileException(ex)
        except Exception as ex:
             raise ProcessFileException(ex)
        finally:
            await redis.aclose()

            end_time = time.time()
            execution_time = end_time - start_time
            logger.info(f"File processed in {execution_time:.4f} seconds. {processed_items} boletos created.")
        