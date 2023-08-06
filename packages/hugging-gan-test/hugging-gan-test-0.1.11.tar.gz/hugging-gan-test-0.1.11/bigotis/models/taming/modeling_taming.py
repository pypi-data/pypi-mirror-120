import os
import yaml
import math
import logging
import requests
from typing import *

import torch
import torchvision
import numpy as np
import omegaconf
import PIL
from PIL import Image
from omegaconf import OmegaConf
from forks.taming_transformers.taming.models.vqgan import VQModel
from bigotis.modeling_utils import ImageGenerator

logging.basicConfig(format='%(message)s', level=logging.INFO)


class TamingDecoder(ImageGenerator):
    """
    Image generator that leverages the decoder of VQGAN to 
    optimize images. This code uses the original implementation
    from https://github.com/CompVis/taming-transformers.
    """
    def __init__(
        self,
        device: str = 'cuda',
    ) -> None:
        """
        Downloads the VQGAN model and loads a pre-defined 
        configuration.

        Args:
            device (str, optional): defaults to 'cuda'.
        """
        super().__init__()

        self.supported_loss_types = [
            "cosine_similarity",
            "spherical_distance",
        ]

        if device is not None:
            self.device = device

        modeling_dir = os.path.dirname(os.path.abspath(__file__))
        modeling_cache_dir = os.path.join(modeling_dir, ".modeling_cache")
        os.makedirs(modeling_cache_dir, exist_ok=True)

        modeling_ckpt_path = os.path.join(modeling_cache_dir, 'last.ckpt')
        if not os.path.exists(modeling_ckpt_path):
            modeling_ckpt_url = 'https://heibox.uni-heidelberg.de/f/867b05fc8c4841768640/?dl=1'

            logging.info(
                f"Downloading pre-trained weights for VQ-GAN from {modeling_ckpt_url}"
            )
            results = requests.get(modeling_ckpt_url, allow_redirects=True)

            with open(modeling_ckpt_path, "wb") as ckpt_file:
                ckpt_file.write(results.content)

        # TODO: update the url with our own config using the correct paths
        modeling_config_path = os.path.join(modeling_cache_dir, 'model.yaml')
        if not os.path.exists(modeling_config_path):
            modeling_config_url = 'https://raw.githubusercontent.com/vipermu/taming-transformers/master/configs/custom_vqgan.yaml'

            logging.info(
                "Downloading `model.yaml` from vipermu taming-transformers fork"
            )
            results = requests.get(modeling_config_url, allow_redirects=True)

            with open(modeling_config_path, "wb") as yaml_file:
                yaml_file.write(results.content)

        vqgan_config_xl = self.load_config(
            config_path=modeling_config_path,
            display=False,
        )
        self.vqgan_model = self.load_vqgan(
            vqgan_config_xl,
            ckpt_path=modeling_ckpt_path,
        ).to(self.device)

    @staticmethod
    def load_config(
        config_path: str,
        display=False,
    ) -> omegaconf.dictconfig.DictConfig:
        """
        Loads a VQGAN configuration file from a path or URL.

        Args:
            config_path (str): local path or URL of the config file.
            display (bool, optional): if `True` the configuration is 
                printed. Defaults to False.

        Returns:
            omegaconf.dictconfig.DictConfig: configuration dictionary.
        """
        config = OmegaConf.load(config_path)

        if display:
            logging.info(yaml.dump(OmegaConf.to_container(config)))

        return config

    @staticmethod
    def load_vqgan(
        config: omegaconf.dictconfig.DictConfig,
        ckpt_path: str = None,
    ) -> VQModel:
        """
        Load a VQGAN model from a config file and a ckpt path 
        where a VQGAN model is saved.

        Args:
            config ([type]): VQGAN model config.
            ckpt_path ([type], optional): path of a saved model. 
                Defaults to None.

        Returns:
            VQModel: 
                loaded VQGAN model.
        """
        model = VQModel(**config.model.params)

        if ckpt_path is not None:
            # XXX: check wtf is going on here
            sd = torch.load(ckpt_path, map_location="cpu")["state_dict"]
            missing, unexpected = model.load_state_dict(sd, strict=False)

        return model.eval()

    def generate_from_prompt(
        self,
        prompt: str,
        lr: float = 0.5,
        target_img_size: int = 256,
        num_steps: int = 200,
        num_augmentations: int = 32,
        init_img_path: str = None,
        loss_type: str = 'cosine_similarity',
        loss_clip_value: float = None,
        generation_cb=None,
        **kwargs,
    ) -> Tuple[List[PIL.Image.Image], List[torch.Tensor]]:
        """
        Returns a list of images generated while optimizing the
        input of a pre-trained VQGAN decoder with a prompt.

        Args:
            prompt (str): input prompt.
            lr (float, optional): learning rate. Defaults to 0.5.
            target_img_size (int, optional): image size of the 
                generated images. Defaults to 256.
            num_steps (int, optional): number of optimization 
                steps. Defaults to 200.
            num_augmentations (int, optional): number of augmented 
                images to use. Defaults to 20.
            init_img_path (str, optional): path for an image to use
                as the starting point of the optimization. Defaults 
                to None.
            loss_type (str, optional): either 'cosine_similarity' 
                or 'spherical_distance'. Defaults to 
                'cosine_similarity'.
            loss_clip_value (float, optional): thresholding value for
                for the CLIP embeddings. Defaults to None.
            generation_cb (function, optional): if provided, the 
                function is executed for every optimization step. The
                inputs of this function will be the generated image
                from the VQGAN (Nx3xHxW) and the logits used to 
                generate it (Nx256xDxD) and the optimization step.

        Returns:
            Tuple[List[PIL.Image.Image], List[torch.Tensor]]: list 
                of optimized images and their respective logits.
        """
        # TODO: implement batching
        batch_size = 1

        target_img_size = target_img_size
        embed_size = target_img_size // 16

        if loss_type not in self.supported_loss_types:
            print(
                (f"ERROR! Loss type {loss_type} not recognized. "
                 f"Only {' or '.join(self.supported_loss_types)} supported."))

            return

        z_logits = .5 * torch.randn(
            batch_size,
            256,
            embed_size,
            embed_size,
        ).to(self.device)

        if init_img_path is None:
            z_logits = torch.nn.Parameter(
                torch.sinh(1.9 * torch.arcsinh(z_logits)), )
        else:
            pil_img = Image.open(init_img_path)
            pil_img = pil_img.convert('RGB')

            init_img = torch.tensor(np.asarray(pil_img)).to(
                self.device).float()[None, :]
            init_img = (init_img / 255.) * 2 - 1
            init_img = init_img.permute(0, 3, 1, 2)

            # clip_img_z_logits = self.get_clip_img_encodings(init_img)
            # clip_img_z_logits = clip_img_z_logits.detach().clone()

            z, _, [_, _, _indices] = self.vqgan_model.encode(init_img)

            z_logits = torch.nn.Parameter(z)
            # img_z_logits = z.detach().clone()

        torch.nn.Parameter(torch.ones((4, )))

        optimizer = torch.optim.AdamW(
            params=[z_logits],
            lr=lr,
            betas=(0.9, 0.999),
            weight_decay=0.1,
        )

        gen_img_list = []
        z_logits_list = []
        for step in range(num_steps):
            loss = 0

            z_logits_list.append(z_logits.detach().clone())

            z = self.vqgan_model.post_quant_conv(z_logits)
            x_rec = self.vqgan_model.decoder(z)
            x_rec = (x_rec.clip(-1, 1) + 1) / 2
            x_rec_stacked = self.augment(
                x_rec,
                num_crops=num_augmentations,
                target_img_width=target_img_size,
                target_img_height=target_img_size,
            )

            loss += 10 * self.compute_clip_loss(
                x_rec_stacked,
                prompt,
                loss_type,
                loss_clip_value,
            )

            # if init_img is not None:
            #     loss += -10 * torch.cosine_similarity(z_logits,
            #                                           img_z_logits).mean()
            # if init_img is not None:
            #     loss += -10 * torch.cosine_similarity(
            #         self.get_clip_img_encodings(x_rec), clip_img_z_logits).mean()

            logging.info(f"\nIteration {step} of {num_steps}")
            logging.info(f"Loss {round(float(loss.data), 2)}")

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            x_rec_img = torchvision.transforms.ToPILImage(mode='RGB')(x_rec[0])
            gen_img_list.append(x_rec_img)

            if generation_cb is not None:
                generation_cb(
                    x_rec,
                    z_logits,
                    step,
                )

            torch.cuda.empty_cache()

        return gen_img_list, z_logits_list

    def interpolate(
        self,
        z_logits_list: List[torch.Tensor],
        duration_list: List[float],
        **kwargs,
    ) -> List[PIL.Image.Image]:
        """
        Returns a list of PIL images corresponding to the 
        generations produced by interpolating the values
        from `z_logits_list`.

        Args:
            z_logits_list (List[torch.Tensor]): list of VQVAE 
                intermediate embeddings.
            duration_list (List[float]): list with the duration of
                the interpolation between each consecutive tensor. 
                The last value represent the duration between the 
                last tensor and the initial.

        Returns:
            List[PIL.Image.Image]: list of the resulting generated images.
        """
        gen_img_list = []
        fps = 25

        for idx, (z_logits,
                  duration) in enumerate(zip(z_logits_list, duration_list)):
            num_steps = int(duration * fps)
            z_logits_1 = z_logits
            z_logits_2 = z_logits_list[(idx + 1) % len(z_logits_list)]

            for step in range(num_steps):
                weight = math.sin(1.5708 * step / num_steps)**2
                z_logits = weight * z_logits_2 + (1 - weight) * z_logits_1

                z = self.vqgan_model.post_quant_conv(z_logits)
                x_rec = self.vqgan_model.decoder(z)
                x_rec = (x_rec.clip(-1, 1) + 1) / 2

                x_rec_img = torchvision.transforms.ToPILImage(mode='RGB')(
                    x_rec[0])
                gen_img_list.append(x_rec_img)

                torch.cuda.empty_cache()

        return gen_img_list


if __name__ == '__main__':
    target_img_size = 256
    prompt = "A pink dog"
    lr = 0.5
    num_steps = 200
    num_augmentations = 128
    loss_type = 'cosine_similarity'
    init_img_path = None
    # init_img_path = "alien.png"
    loss_clip_value = None

    def save_img_cb(
        x_rec,
        _z_logits,
        step,
    ):
        x_rec_img = torchvision.transforms.ToPILImage(mode='RGB')(x_rec[0])
        x_rec_img.save(f"{step}.jpg")

    taming_decoder = TamingDecoder()
    gen_img_list, z_logits_list = taming_decoder.generate_from_prompt(
        prompt=prompt,
        lr=lr,
        target_img_size=target_img_size,
        num_steps=num_steps,
        num_augmentations=num_augmentations,
        init_img_path=init_img_path,
        loss_type=loss_type,
        loss_clip_value=loss_clip_value,
        generation_cb=save_img_cb,
    )

    # _gen_img_list, z_logits_list_ = taming_decoder.generate_from_prompt(
    #     prompt="Pokemon of type grass",
    #     lr=lr,
    #     num_steps=num_steps,
    #     num_augmentations=num_augmentations,
    #     init_img_path=init_img_path,
    # )

    # z_logits_interp_list = [z_logits_list[-1], z_logits_list_[-1]]

    # duration_list = [0.7] * len(z_logits_interp_list)
    # interpolate_img_list = taming_decoder.interpolate(
    #     z_logits_list=z_logits_interp_list,
    #     duration_list=duration_list,
    # )
