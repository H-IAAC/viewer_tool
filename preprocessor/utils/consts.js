const path = require('path');

PREPROCESSING_DIR = '';
POSTPROCESSING_DIR = '';

PREPROCESSING_STATIC = '/pre';
POSTPROCESSING_STATIC = '/pos';

CONFIG_FILE_PATH = path.join(__dirname + path.sep + '..' + path.sep + 'config/config.json');

module.exports = {PREPROCESSING_DIR, POSTPROCESSING_DIR, PREPROCESSING_STATIC, POSTPROCESSING_STATIC, CONFIG_FILE_PATH};
