import threading
import logging
import time
import random
import shutil
import os


def simulate_incoming_images():
    def copy_image(seconds):
        while True:
            try:
                time.sleep(seconds)
                filename = str(random.randint(1000, 9999)) + ".jpg"
                shutil.copyfile("/data/asd.jpg", "/data/" + filename)
                logging.info("[SIMULATOR] created image to /data/" + filename)
            except KeyboardInterrupt:
                logging.info("Image watcher interrupted")
                break

    # run copy_image in the background every 3 sedonds
    t = threading.Thread(target=copy_image, args=(3,))
    t.start()


def deleting_images():
    def delete_images(seconds):
        while True:
            try:
                time.sleep(seconds)
                for file in os.listdir("/data"):
                    if file != "asd.jpg":
                        os.remove("/data/" + file)
                        logging.info("[DELETER] deleted image from /data/" + file)
            except KeyboardInterrupt:
                logging.info("Image watcher interrupted")
                break

    t2 = threading.Thread(target=delete_images, args=(30,))
    t2.start()


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)
    logger.info("[SIMULATOR] Starting simulator")
    simulate_incoming_images()
    deleting_images()
    while True:
        try:
            time.sleep(60)
        except KeyboardInterrupt:
            logging.info("Image watcher interrupted")
            break
