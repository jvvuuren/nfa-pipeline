#Use this script to create your pipelineConfig.cfg
import ConfigParser

config = ConfigParser.RawConfigParser()

config.add_section('Directories')
config.set('Directories', "pipelinePath", "<PIPELINE_PATH>")
config.set('Directories', "rootDir", "<ROOT_DIR>")
config.set('Directories', "writeRootDir", "<WRITE_ROOT_DIR>")

config.add_section('Shotgun')
config.set('Shotgun', 'shotgun_url', r"<SHOTGUN_URL>")
config.set('Shotgun', 'api_key', r"<API_KEY>")

# Writing our configuration file
with open('pipelineConfig.cfg', 'wb') as configfile:
    config.write(configfile)