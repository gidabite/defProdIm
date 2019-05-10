import configparser as cp
import os

default_path = "config.ini"


def get_config(path=None):
    config = cp.ConfigParser()
    if path is not None:
        config.read(path)
    else:
        if not os.path.exists(default_path):

            config["General"] = {
                "threshold_ration": "2.0"
            }

            config["Logging"] = {
                "text_log": "True",
                "img_log": "True",
                "show_img": "False",
                "log_path": "../log/{date_time}/"
            }

            config["SearchItem"] = {
                "image_scale_factor": "0.1",
                "max_area": "3000.1",
                "gaussian_kernel": "(3, 3)",
                "close_kernel": "(7, 7)",
                "sigma": "0.1"
            }

            config["Barcode"] = {
                "enabled": "True",
                "margin_x": "15",
                "margin_y": "15"
            }

            config["Color"] = {
                "enabled": "True",
                "count_samples": 1000
            }

            config["Size"] = {
                "enabled": "True",
                "scale": "0.0001118223"
            }

            config["Neural"] = {
                "enabled": "True"
            }
            with open(default_path, "w") as config_file:
                config.write(config_file)

        config.read(default_path)
    return config
