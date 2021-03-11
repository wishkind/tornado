
import asyncio
import logging
import signal

import tornado.platform.asyncio

import app
import settings


logger = logging.getLogger(__name__)


def stop_handler():
    logger.info('interrupt signal received, shutting down')
    loop = asyncio.get_event_loop()

    try:
        # loop.run_until_complete(app.stop())
        # loop.run_until_complete(loop.shutdown_asyncgens())
        loop.stop()
        loop.close()

    except RuntimeError:
        pass


def configure_signals():
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, stop_handler)
    loop.add_signal_handler(signal.SIGTERM, stop_handler)


def configure_logging():
    logging.basicConfig(
        filename=None,
        level=settings.LOG_LEVEL,
        format='%(asctime)s: %(levelname)7s: [%(name)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def configure_tornado():
    # install asyncio loop
    tornado.platform.asyncio.AsyncIOMainLoop().install()


if __name__ == '__main__':
    configure_signals()
    configure_logging()
    configure_tornado()

    logger.info('Started Lateral API Server')

    loop = asyncio.get_event_loop()
    loop.create_task(app.run())
    loop.run_forever()

    logger.info('Server Stopped!!!')


