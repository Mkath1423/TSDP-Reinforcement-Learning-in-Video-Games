import os
import yaml


# utility wrappers
def exists(path, log=None, msg="", supress_warning=False):
    out = os.path.exists(path)
    if log is not None and not out and not supress_warning:
        log.warning(f"path: {path} does not exist." + msg)
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


def make_dirs(path, log=None, msg="", supress_warning=False):
    try:
        os.makedirs(os.path.dirname(path))

    except OSError as e:
        if log is not None and not supress_warning:
            log.error("directory all ready exists: " + msg + "\n" + str(e))
        return False

    return True


# file read write
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


def save_yaml(data, path, log=None, default_flow_style=False):
    made_dir = make_dirs(path, supress_warning=True)

    msg = f"Save file to {path}" + " made dirs that did not exist" if made_dir else ""
    if log is not None:
        log.info(msg)

    with open(path, "w") as f:
        yaml.dump(data, stream=f, default_flow_style=default_flow_style)


# training checkpoints
# pass

if __name__ == "__main__":
    _data = {
        "agents": [dict([
            (["hp", "x", 'y', 'move'][n], n * (i + 1)) for n in range(4)
        ]) for i in range(3)],
        "bullets": [dict([
            (["x", 'y', 'dir'][n], n * (i + 1)) for n in range(3)
        ]) for i in range(5)]
    }

    save_yaml(data, r"a\b\test.yaml")
