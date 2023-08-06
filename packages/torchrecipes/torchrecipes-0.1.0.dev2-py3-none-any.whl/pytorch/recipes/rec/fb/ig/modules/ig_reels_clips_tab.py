#!/usr/bin/env python3
import os

import pytorch_lightning as pl
import torch
import torch.distributed as dist


class IGReelsClipsTab(pl.LightningModule):
    def __init__(
        self,
    ) -> None:
        super().__init__()

        rank = int(os.environ["LOCAL_RANK"])
        if torch.cuda.is_available():
            device = torch.device(f"cuda:{rank}")
            backend = "nccl"
            torch.cuda.set_device(device)
        else:
            device = torch.device("cpu")
            backend = "gloo"

        dist.init_process_group(backend=backend)
        self.to(device=device)
