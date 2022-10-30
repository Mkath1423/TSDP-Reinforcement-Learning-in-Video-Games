import os
import yaml


def exists(path, log=None, msg="", supress_warning=False):
    out = os.path.exists(path)
    if log is not None and not out and not supress_warning:
        log.warning(f"path: {path} does not exist." + msg)
        log.warning(f"path does not exist")
    return out


def is_dir(path, log=None, msg="", supress_warning=False):
    out = os.path.isdir(path)
    if log is not None and not out and not supress_warning:
        log.warning(f"expected path: {path} to be a dir, but it is not." + msg)

    return out


def is_file(path, log=None, msg="", supress_warning=False):
    out = os.path.isfile(path)
    if log is not None and not out and not supress_warning:
        log.warning(f"expected path: {path} to be a file, but it is not." + msg)

    return out


def load_yaml(path, log=None):
    if not exists(path, log=log, msg=". Failed to load yaml.") or \
            not is_file(path, log=log, msg=". Failed to load yaml."):
        return None

    with open(path, "r") as f:
        try:
            return yaml.safe_load(f)

        except yaml.YAMLError as e:
            msg = "Error while parsing YAML file.\n"
            if hasattr(e, 'problem_mark'):
                if e.context is not None:
                    msg += f"\tparser says\n{str(e.problem_mark)}\n{str(e.problem)} {str(e.context)}\nPlease correct data and retry."
                else:
                    msg += f"\tparser says\n{str(e.problem)} {str(e.context)}\nPlease correct data and retry."

            if log is not None:
                log.error(msg)

            return None


if __name__ == "__main__":
    print(load_yaml("../config/logger.yaml"))