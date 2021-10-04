import logging

def setup_log():
    logger = logging.getLogger('AppLog')
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('app.log')
    fh.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.WARNING)

    fhFormatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    shFormatter = logging.Formatter('%(levelname)s - %(filename)s - Line: %(lineno)d - %(message)s')
    fh.setFormatter(fhFormatter)
    sh.setFormatter(shFormatter)

    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
