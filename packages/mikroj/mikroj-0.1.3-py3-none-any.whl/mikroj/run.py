import numpy
from mikroj.helper import ImageJHelper
from mikro.schema import Representation, RepresentationVariety
from arkitekt import AppAgent, agents, use
import argparse
import xarray as xr
import numpy as np
from mikroj.implementations.temp_color_code import color_code

parser = argparse.ArgumentParser()
parser.add_argument('--config', help='Which config file to use', default="bergen.yaml", type=str)
args = parser.parse_args()



def main():
    print(args)

    bergen_params = {
        "config_path": args.config
    }

    agent = AppAgent(**bergen_params)

    helper = ImageJHelper()


    @agent.register()
    def show(rep: Representation) -> Representation:
        """Show

        Shows the Image on MikroJ

        Args:
            rep (Representation): [description]

        Returns:
            Representation: [description]
        """
        helper.displayRep(rep)
        return rep

    @agent.register()
    def color_coder(rep: Representation) -> Representation:
        """Color Code Z

        Runs the Image Macro Color Code 

        Args:
            rep (Representation): The Image Coming in

        Returns:
            Representation: The Color Coded Image
        """
        image = color_code(rep.data)
        return Representation.objects.from_xarray(image, sample=rep.sample, meta=rep.meta, variety=RepresentationVariety.VOXEL, tags=["rgb"], name=f"Color Code of {rep.name}")

    agent.provide()


if __name__ == "__main__":
    main()








