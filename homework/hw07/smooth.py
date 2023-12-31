# -*- coding: utf-8 -*-

# ********************************** #
# Author: kaanguney.keklikci@tum.de  #
# Date: 06.07.2023                   #
# ********************************** #

import numpy as np
import tifffile
import matplotlib.pyplot as plt
import os
import aomip


def main():
    N = 512
    os.makedirs("images", exist_ok=True)
    export = plt.imshow(aomip.smooth(512))
    plt.axis("off")
    plt.colorbar(export)
    plt.tight_layout()
    plt.savefig("images/notebook/smooth.png")


if __name__ == "__main__":
    main()
