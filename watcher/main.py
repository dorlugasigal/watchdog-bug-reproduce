import time
import logging
import threading
from watchdog.events import RegexMatchingEventHandler
from watchdog.observers.polling import PollingObserver


class ImagesEventHandler(RegexMatchingEventHandler):
    IMAGES_REGEX = [r"(.*).(jpe?g|bmp)$"]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super().__init__(self.IMAGES_REGEX)
        self.logger.info("[HANDLER] Starting image processing")

    def on_created(self, event):
        self.logger.info("[HANDLER] New image found: %s" % event.src_path)


class MyObserver:
    """ Observes the monitored folders for new images and processes them with the event handler. """

    def __init__(
        self,
        observer: PollingObserver,
        handler: ImagesEventHandler,
    ):
        self._logger = logging.getLogger(__name__)
        self._logger.info("[WATCHER] Starting image watcher")
        self._event_handler = handler
        self._event_observer = observer

    def watch(self):
        """Start the observer and watch for new images in the monitored folders. """
        self._start()
        while True:
            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self._logger.info("[WATCHER] Image watcher interrupted")
                self._stop()
                break
            except Exception as err:
                self._logger.error(
                    f"[WATCHER] Unexpected Exception thrown {err}")

    def _start(self):
        self._logger.info("[WATCHER] Image watcher started")
        self._schedule()
        self._event_observer.start()

    def _stop(self):
        self._logger.info("[WATCHER] Image watcher stopped")
        self._event_observer.stop()
        self._event_observer.join()

    def _schedule(self):
        self._logger.info("[WATCHER] Begin watching: /data")
        self._event_observer.schedule(
            self._event_handler, path="/data", recursive=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    logging.info("[OBSERVER] Starting image watcher")
    MyObserver(PollingObserver(), ImagesEventHandler()).watch()
