import os
import threading

import pandas as pd

from pylighter import Annotation, config
from pylighter import display as display_helper
from pylighter import utils
from pylighter.chunk_models import Chunk, Chunks
from pylighter.shortcut_helper import shortcut_helper


class Merge:
    """
    Class used to merge multiple annotations
    """

    def __init__(
        self,
        annotations: List[Annotation],
        merge_save_path=config.ANNOTATION_SAVE_PATH,
        labels_names=config.LABELS_NAMES,
        labels_colors=config.DEFAULT_COLORS,
        standard_shortcuts=config.SHORTCUTS,
        char_params=config.CHAR_PARAMS,
    ):

        # Check input consistency
        utils.assert_input_consistency(corpus, labels, start_index)
