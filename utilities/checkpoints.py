import os
import torch
from torch import nn


# https://pytorch.org/tutorials/recipes/recipes/saving_and_loading_a_general_checkpoint.html
# MODEL_PATH = "/content/drive/MyDrive/ColabData/Unet2"

def check_load_path(path):
    if not os.path.isfile(path):
        print("ERROR: checkpoint with this name does not exists:\n", path)
        return False
    return True


def check_save_path(path, overwrite):
    if os.path.exists(path) and not overwrite:
        print("ERROR: checkpoint with this name already exists. call with overwrite = True to overwrite existing files")
        return False
    if os.path.exists(path):
        print("WARNING: checkpoint with this name already exists... overwriting")

    elif not os.path.isdir(os.path.dirname(path)):
        print("WARNING: folder does not exist:")
        print("\t" + "making new folder: " + os.path.dirname(path))
        os.makedirs(os.path.dirname(path))

    return True


# Save and load checkpoint
def load_pt(path):
    if check_load_path(path):
        print("loading checkpoint:\n", path)
        return True, torch.load(path)

    return False, None


def save_pt(path, obj, overwrite=False):
    if check_save_path(path, overwrite):
        print("saving checkpoint:\n", path)
        torch.save(obj, path)
        return True

    return False


def load_checkpoint(path):
    if check_load_path(path):
        valid, checkpoint = load_pt(path)

        return valid, checkpoint["model"], \
            checkpoint["optimizer"], \
            {k: v for (k, v) in checkpoint.items() if k not in ["model", "optimizer"]}

    return False, None, None, None


def save_checkpoint(path, model, optimizer, overwrite=False, **kwargs):
    if check_save_path(path, overwrite):
        torch.save(
            dict(
                [("model", model.state_dict()),
                 ("optimizer", optimizer.state_dict)] +
                list(kwargs.items())
            ),
            path
        )


def load_script(path):
    if check_load_path(path):
        print("loading checkpoint:\n", path)
        return True, torch.jit.load(path)

    return False, None


def save_script(path, model, overwrite=False, ):
    # You must call model.eval() to set dropout and batch normalization layers to evaluation mode before running inference.
    # Failing to do this will yield inconsistent inference results.
    # If you wish to resuming training, call model.train() to ensure these layers are in training mode.
    if check_save_path(path, overwrite):
        print("saving torch script:\n", path)

        scripted_module = torch.jit.script(model)
        torch.jit.save(scripted_module, 'path')

        return True

    return False
