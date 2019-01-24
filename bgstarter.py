from core.Application import Application
from core.BackgroundSession import BackgroundSession
import logging
import nltk as nk

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    print('running')

    nk.download("stopwords")
    nk.download("punkt") # needed for removing punctuations.
    nk.download('averaged_perceptron_tagger')   # required by the pos tagger.
    nk.download("wordnet")


    bgSession = Application.OpenBackgroundSession()
    logger.info('bgSession created.')
    bgSession.run()
    bgSession.closeSession()
