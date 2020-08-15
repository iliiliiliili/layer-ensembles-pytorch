from networks.vgg import createVGG
from networks.variational import (
    VariationalBase,
    VariationalConvolution,
    VariationalLinear,
)
from networks.classic import ClassicConvolution, ClassicLinear
from networks.dropout import DropoutConvolution, DropoutLinear
from typing import Optional
from core import give, rename_dict
import torch
from torchvision import datasets, transforms
from networks.network import Network
import os
import fire  # type:ignore
import json

from networks.mnist_base import createMnistBase
from networks.cifar10_base import createCifar10Base
from networks.resnet import createResnet

dataset_params = {
    "mnist": {
        "mean": (0.1307,),
        "std": (0.3081,),
        "dataset": datasets.MNIST,
        "path": "./datasets/",
        "train_size": 50000,
        "validation_size": 10000,
    },
    "cifar10": {
        "mean": (0.5, 0.5, 0.5),
        "std": (0.5, 0.5, 0.5),
        "dataset": datasets.CIFAR10,
        "path": "./datasets/",
        "train_size": 40000,
        "validation_size": 10000,
    },
}


networks = {
    "mnist_base_vnn": createMnistBase(
        VariationalConvolution, VariationalLinear
    ),
    "mnist_base_classic": createMnistBase(
        ClassicConvolution, ClassicLinear
    ),
    "mnist_base_dropout": createMnistBase(
        DropoutConvolution, DropoutLinear
    ),

    "cifar10_base_vnn": createCifar10Base(
        VariationalConvolution, VariationalLinear
    ),
    "cifar10_base_classic": createCifar10Base(
        ClassicConvolution, ClassicLinear
    ),
    "cifar10_base_dropout": createCifar10Base(
        DropoutConvolution, DropoutLinear
    ),

    "resnet_vnn_18": createResnet(
        VariationalConvolution, VariationalLinear
    )['ResNet18'],
    "resnet_vnn_34": createResnet(
        VariationalConvolution, VariationalLinear
    )['ResNet34'],
    "resnet_vnn_50": createResnet(
        VariationalConvolution, VariationalLinear
    )['ResNet50'],
    "resnet_vnn_101": createResnet(
        VariationalConvolution, VariationalLinear
    )['ResNet101'],
    "resnet_vnn_152": createResnet(
        VariationalConvolution, VariationalLinear
    )['ResNet152'],

    "resnet_classic_18": createResnet(
        ClassicConvolution, ClassicLinear
    )['ResNet18'],
    "resnet_classic_34": createResnet(
        ClassicConvolution, ClassicLinear
    )['ResNet34'],
    "resnet_classic_50": createResnet(
        ClassicConvolution, ClassicLinear
    )['ResNet50'],
    "resnet_classic_101": createResnet(
        ClassicConvolution, ClassicLinear
    )['ResNet101'],
    "resnet_classic_152": createResnet(
        ClassicConvolution, ClassicLinear
    )['ResNet152'],

    "resnet_dropout_18": createResnet(
        DropoutConvolution, DropoutLinear
    )['ResNet18'],
    "resnet_dropout_34": createResnet(
        DropoutConvolution, DropoutLinear
    )['ResNet34'],
    "resnet_dropout_50": createResnet(
        DropoutConvolution, DropoutLinear
    )['ResNet50'],
    "resnet_dropout_101": createResnet(
        DropoutConvolution, DropoutLinear
    )['ResNet101'],
    "resnet_dropout_152": createResnet(
        DropoutConvolution, DropoutLinear
    )['ResNet152'],

    "vgg_vnn_11": createVGG(
        VariationalConvolution, VariationalLinear
    )["VGG11"],
    "vgg_vnn_13": createVGG(
        VariationalConvolution, VariationalLinear
    )["VGG13"],
    "vgg_vnn_16": createVGG(
        VariationalConvolution, VariationalLinear
    )["VGG16"],
    "vgg_vnn_19": createVGG(
        VariationalConvolution, VariationalLinear
    )["VGG19"],

    "vgg_classic_11": createVGG(
        ClassicConvolution, ClassicLinear
    )["VGG11"],
    "vgg_classic_13": createVGG(
        ClassicConvolution, ClassicLinear
    )["VGG13"],
    "vgg_classic_16": createVGG(
        ClassicConvolution, ClassicLinear
    )["VGG16"],
    "vgg_classic_19": createVGG(
        ClassicConvolution, ClassicLinear
    )["VGG19"],

    "vgg_dropout_11": createVGG(
        DropoutConvolution, DropoutLinear
    )["VGG11"],
    "vgg_dropout_13": createVGG(
        DropoutConvolution, DropoutLinear
    )["VGG13"],
    "vgg_dropout_16": createVGG(
        DropoutConvolution, DropoutLinear
    )["VGG16"],
    "vgg_dropout_19": createVGG(
        DropoutConvolution, DropoutLinear
    )["VGG19"],
}

loss_functions = {
    "cross_entropy": torch.nn.CrossEntropyLoss(),
    "mse": torch.nn.MSELoss(),
}

activations = {
    "relu": torch.nn.ReLU,
    "relu6": torch.nn.ReLU6,
    "sigmoid": torch.nn.Sigmoid,
    "tanh": torch.nn.Tanh,
    "leacky_relu": torch.nn.LeakyReLU,
}

activation_params = {
    "relu": ["inplace"],
    "relu6": ["inplace"],
    "sigmoid": [],
    "tanh": [],
    "leacky_relu": ["negative_slope", "inplace"],
}


def create_train_validation_test(dataset_name: str):

    params = dataset_params[dataset_name]

    train_val = params["dataset"](
        params["path"],
        train=True,
        download=True,
        transform=transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize(params["mean"], params["std"]),
            ]
        ),
    )

    test = params["dataset"](
        params["path"],
        train=False,
        download=True,
        transform=transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize(params["mean"], params["std"]),
            ]
        ),
    )

    train, val = torch.utils.data.random_split(  # type: ignore
        train_val, [params["train_size"], params["validation_size"]]
    )

    return train, val, test


def get_best_description(path):
    if os.path.exists(path):
        with open(path) as file:
            data = json.load(file)
            return data
    else:
        return None


def correct_count(output, target):
    labels = output.data.max(1, keepdim=True)[1]
    return labels.eq(target.data.view_as(labels)).sum()


def run_evaluation(net: Network, val, device, correct_count, batch):

    print()

    net.eval()
    VariationalBase.GLOBAL_STD = 0

    total_correct = 0
    total_elements = 0

    for i, (data, target) in enumerate(val):

        data = data.to(device)
        target = target.to(device)

        loss, correct = net.eval_step(
            data, target, correct_count=correct_count
        )

        total_correct += correct
        total_elements += batch

        print(
            "eval s["
            + str(i + 1)
            + "/"
            + str(len(val))
            + "]"
            + " loss="
            + str(loss)
            + " acc="
            + str(float(total_correct) / total_elements),
            end="\r",
        )

    print()

    net.train()
    return float(total_correct) / total_elements


def evaluate(
    network_name,
    dataset_name,
    batch=1,
    model_path=None,
    model_suffix="",
    split="validation",
    device="cuda:0",
    **kwargs,
):

    if model_path is None:

        full_network_name = network_name

        if dataset_name not in network_name:
            full_network_name = dataset_name + "_" + full_network_name

        full_network_name += "" if model_suffix == "" else "_" + model_suffix

        model_path = "./models/" + full_network_name

    device = torch.device(device if torch.cuda.is_available() else "cpu")

    net: Network = networks[network_name](**kwargs)

    train, val, test = create_train_validation_test(dataset_name)

    current_dataset = {"train": train, "validation": val, "test": test}[split]

    result = run_evaluation(net, current_dataset, device, correct_count, batch)

    print('Evaluation on "' + split + '" result: ' + str(result))

    with open(model_path + "/results/eval_" + split + ".txt", "w") as f:
        f.write(str(result) + "\n")


def train(
    network_name,
    dataset_name,
    batch,
    epochs,
    model_path=None,
    model_suffix="",
    save_steps=-1,
    validation_steps=-1,
    learning_rate=0.0001,
    momentum=0.9,
    loss_function_name="cross_entropy",
    device="cuda:0",
    save_best=True,
    start_global_std: Optional[float] = None,
    end_global_std: Optional[float] = None,
    **kwargs,
):

    if "activation" in kwargs:

        current_activations = kwargs["activation"].split(" ")
        activation_functions = []

        for i, activation in enumerate(current_activations):

            activation_kwargs, kwargs = give(
                kwargs,
                list(
                    map(
                        lambda a: activation + "_" + a,
                        activation_params[activation],
                    )
                ),
            )

            if activation in current_activations[i + 1:]:
                kwargs = {**kwargs, **activation_kwargs}

            func = activations[activation](
                **rename_dict(
                    activation_kwargs,
                    lambda name: name.replace(activation + "_", ""),
                )
            )

            activation_functions.append(func)

        if len(activation_functions) == 1:
            activation_functions = activation_functions[0]

        kwargs["activation"] = activation_functions

    if model_path is None:

        full_network_name = network_name

        if dataset_name not in network_name:
            full_network_name = dataset_name + "_" + full_network_name

        full_network_name += "" if model_suffix == "" else "_" + model_suffix

        model_path = "./models/" + full_network_name

    if not os.path.exists(model_path):
        os.mkdir(model_path)
    if not os.path.exists(model_path + "/results"):
        os.mkdir(model_path + "/results")
    if not os.path.exists(model_path + "/best"):
        os.mkdir(model_path + "/best")

    device = torch.device(device if torch.cuda.is_available() else "cpu")

    net: Network = networks[network_name](**kwargs)

    train, val, _ = create_train_validation_test(dataset_name)

    train = torch.utils.data.DataLoader(  # type: ignore
        train, batch, shuffle=True, num_workers=4
    )

    val = torch.utils.data.DataLoader(  # type: ignore
        val, batch, shuffle=False, num_workers=4
    )

    if save_steps < 0:
        save_steps = -save_steps * len(train)

    if validation_steps < 0:
        validation_steps = -validation_steps * len(train)

    net.prepare_train(
        learning_rate=learning_rate,
        momentum=momentum,
        loss_func=loss_functions[loss_function_name],
    )
    net.to(device)

    steps_count = len(train) * epochs

    def run_train():
        net.train()

        current_step = 0

        for epoch in range(epochs):

            total_correct = 0
            total_elements = 0

            for i, (data, target) in enumerate(train):

                if start_global_std is not None:
                    VariationalBase.GLOBAL_STD = start_global_std + (
                        current_step / steps_count
                    ) * (end_global_std - start_global_std)

                data = data.to(device)
                target = target.to(device)

                current_step += 1
                loss, correct = net.train_step(
                    data, target, correct_count=correct_count
                )

                total_correct += correct
                total_elements += batch

                log = (
                    full_network_name
                    + " e["
                    + str(epoch + 1)
                    + "/"
                    + str(epochs)
                    + "]"
                    + " s["
                    + str(i + 1)
                    + "/"
                    + str(len(train))
                    + "]"
                    + " loss="
                    + str(loss)
                    + " acc="
                    + str(float(total_correct) / total_elements)
                )

                if start_global_std is not None:
                    log += " g_std=" + str(VariationalBase.GLOBAL_STD)

                print("{:<80}".format(log), end="\n")

                if current_step % save_steps == 0:
                    net.save(model_path)

                if current_step % validation_steps == 0:
                    val_acc = run_evaluation(
                        net, val, device, correct_count, batch
                    )

                    if validation_steps % len(train) == 0:
                        text = "epoch " + str(epoch + 1) + ": "
                    else:
                        text = "step " + str(current_step) + ": "

                    text += str(val_acc)

                    with open(
                        model_path
                        + "/results/validation_batch_"
                        + str(batch)
                        + ".txt",
                        "a",
                    ) as f:
                        f.write(text)

                    best_description = get_best_description(
                        model_path + "/best/description.json"
                    )

                    is_should_save_best = False

                    if best_description is None:
                        is_should_save_best = True
                    else:
                        is_should_save_best = (
                            best_description["result"] * 1.001 < val_acc
                        )

                    if is_should_save_best and save_best:
                        print(":::Saving Best:::")

                        net.save(model_path + "/best")

                        data = {
                            "epoch": epoch + 1,
                            "batch": batch,
                            "result": val_acc,
                        }

                        with open(
                            model_path + "/best/description.json", "w"
                        ) as file:
                            json.dump(data, file)

                        print(":::Saved Best:::")

    run_train()


if __name__ == "__main__":

    fire.Fire()
