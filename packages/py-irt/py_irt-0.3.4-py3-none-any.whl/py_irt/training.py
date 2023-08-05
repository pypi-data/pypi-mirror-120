from typing import Optional, Union, Dict
from pathlib import Path

import typer
import torch

from pyro.infer import SVI, Trace_ELBO
import pyro

from rich.console import Console
from rich.live import Live
from rich.table import Table

# These imports are necessary to have @register run
# pylint: disable=unused-import
from py_irt.models import (
    abstract_model,
    one_param_logistic,
    two_param_logistic,
    four_param_logistic,
    multidim_2pl,
)
from py_irt.io import safe_file, write_json
from py_irt.dataset import Dataset
from py_irt.initializers import INITIALIZERS, IrtInitializer
from py_irt.config import IrtConfig
from py_irt.models.abstract_model import IrtModel


training_app = typer.Typer()
console = Console()


class IrtModelTrainer:
    def __init__(
        self,
        *,
        data_path: Path,
        config: IrtConfig,
        dataset: Optional[Dataset] = None,
        verbose: bool = True,
    ) -> None:
        self._data_path = data_path
        self._config = config
        IrtModel.validate_name(config.model_type)
        self._priors = None
        self._device = None
        self._epochs = None
        self.irt_model: Optional[abstract_model.IrtModel] = None
        self._pyro_model = None
        self._pyro_guide = None
        self._verbose = verbose
        self.best_params = None
        if dataset is None:
            self._dataset = Dataset.from_jsonlines(data_path)
        else:
            self._dataset = dataset

        # filter out test data
        training_idx = [
            i
            for i in range(len(self._dataset.training_example))
            if self._dataset.training_example[i]
        ]
        self._dataset.observation_subjects = [
            self._dataset.observation_subjects[i] for i in training_idx
        ]
        self._dataset.observation_items = [self._dataset.observation_items[i] for i in training_idx]
        self._dataset.observations = [self._dataset.observations[i] for i in training_idx]
        self._dataset.training_example = [self._dataset.training_example[i] for i in training_idx]

        if config.initializers is None:
            initializers = []
        else:
            initializers = config.initializers

        self._initializers = []
        for init in initializers:
            if isinstance(init, IrtInitializer):
                self._initializers.append(init)
            elif isinstance(init, str):
                self._initializers.append(INITIALIZERS[init](self._dataset))
            elif isinstance(init, Dict):
                name = init.pop("name")
                self._initializers.append(INITIALIZERS[name](self._dataset, **init))
            else:
                raise TypeError("invalid initializer type")

    def train(self, *, epochs: Optional[int] = None, device: str = "cpu") -> None:
        model_type = self._config.model_type
        if epochs is None:
            epochs = self._config.epochs
        self._device = device
        self._priors = self._config.priors
        self._epochs = epochs
        args = {
            "device": device,
            "num_items": len(self._dataset.ix_to_item_id),
            "num_subjects": len(self._dataset.ix_to_subject_id),
        }
        # TODO: Find a better solution to this
        if self._config.priors is not None:
            args["priors"] = self._config.priors

        if self._config.dims is not None:
            args["dims"] = self._config.dims

        console.log(f"Parsed Model Args: {args}")
        self.irt_model = IrtModel.from_name(model_type)(**args)
        pyro.clear_param_store()
        self._pyro_model = self.irt_model.get_model()
        self._pyro_guide = self.irt_model.get_guide()
        device = torch.device(device)
        scheduler = pyro.optim.ExponentialLR(
            {
                "optimizer": torch.optim.Adam,
                "optim_args": {"lr": self._config.lr},
                "gamma": self._config.lr_decay,
            }
        )
        svi = SVI(self._pyro_model, self._pyro_guide, scheduler, loss=Trace_ELBO())
        subjects = torch.tensor(self._dataset.observation_subjects, dtype=torch.long, device=device)
        items = torch.tensor(self._dataset.observation_items, dtype=torch.long, device=device)
        responses = torch.tensor(self._dataset.observations, dtype=torch.float, device=device)

        # Don't take a step here, just make sure params are initialized
        # so that initializers can modify the params
        _ = self._pyro_model(subjects, items, responses)
        _ = self._pyro_guide(subjects, items, responses)
        for init in self._initializers:
            init.initialize()
        table = Table()
        table.add_column("Epoch")
        table.add_column("Loss")
        table.add_column("Best Loss")
        table.add_column("New LR")
        loss = float("inf")
        best_loss = loss
        current_lr = self._config.lr
        with Live(table) as live:
            live.console.print(f"Training Pyro IRT Model for {epochs} epochs")
            for epoch in range(epochs):
                loss = svi.step(subjects, items, responses)
                if loss < best_loss:
                    best_loss = loss
                    self.best_params = self.export()
                scheduler.step()
                current_lr = current_lr * self._config.lr_decay
                if epoch % 100 == 0:
                    table.add_row(
                        f"{epoch + 1}", "%.4f" % loss, "%.4f" % best_loss, "%.4f" % current_lr
                    )

            table.add_row(f"{epoch + 1}", "%.4f" % loss, "%.4f" % best_loss, "%.4f" % current_lr)

    def export(self):
        results = self.irt_model.export()
        results["irt_model"] = self._config.model_type
        results["item_ids"] = self._dataset.ix_to_item_id
        results["subject_ids"] = self._dataset.ix_to_subject_id
        return results

    def save(self, output_path: Union[str, Path]):
        write_json(safe_file(output_path), self.export())
