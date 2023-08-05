
"""Layer Class

Three types of layers
- Obstacle Layer
- Trigger Layer
- Render Layer (does nothing more than display content)
"""

# Maybe inherit from Sprite also
# To be able to add in groups


import pygame
import time
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from ipywidgets import interact,FloatSlider,IntSlider


from .rectangle import BaseRectangle
from ..utils.image import snap_mask_to_grid,image3d_to_mask,mask_to_image3d,mask_to_mesh
from ..exceptions import ObjectNotBoundError


class BaseLayer(BaseRectangle):
    def __init__(self,img_filepath,img_transparency = (255,255,255),obstacle = True,trigger = False,mask_threshold = 0.1,init_window = True,**kwargs):

        super().__init__(x = 0,y = 0,img_filepath = img_filepath,img_transparency = img_transparency,**kwargs)

        self._obstacle = obstacle
        self._trigger = trigger
        self._raw_img = Image.open(self.img_filepath)
        self.mask_threshold = mask_threshold
        self.saved_cell_size = 0
    
    def init_internals(self):
        super().init_internals()
        self.mask_array = self.get_mask()
        self.raw_img = np.copy(self.get_img())

    def get_size(self):
        return self._raw_img.size


    @property
    def layer(self):
        return True


    @property
    def obstacle(self):
        return self._obstacle
    
    @property
    def trigger(self):
        return self._trigger


    def save_img(self):
        """Save transformed layer as png for further use
        """
        name = f"Layer_{str(time.time())[:10]}_cellsize={self.saved_cell_size}.png"
        Image.fromarray(self.get_img()).save(name)
        print(f"Saved image as {name}")


    def get_img(self):
        """Get numpy array image from pygame surface
        Axes are swapped between numpy and pygame
        """
        if not hasattr(self,"image"):
            raise ObjectNotBoundError("You need to bind the layer to an environment first, because self.image is not initialized")
        else:
            return pygame.surfarray.array3d(self.image).swapaxes(0,1)

    def get_mask(self):
        """Get mask from image, ie a 2D array with 0 for transparent and 1 for object
        """
        img = self.get_img()
        return image3d_to_mask(img)


    def snap_to_grid(self,threshold = None,cell_size = None,return_3d = False):
        """Snap a mask to a given grid, can be used to transform a layer for a grid environment

        Args:
            threshold (float, optional): Threshold to consider a mask, 0.1 means a box with 10% of 1 will be a 1 . Defaults to None, which will use the attribute .mask_threshold
            cell_size (int, optional): the size for each cell in the grid. Defaults to None, which will take the environment value env.cell_size
            return_3d (bool, optional): Returns the array as 3D numpy array or 2D mask. Defaults to False.

        Returns:
            np.ndarray: The mask snapped to a grid
        """

        if threshold is None: threshold = self.mask_threshold
        if cell_size is None: cell_size = self.env.cell_size

        mask = snap_mask_to_grid(self.mask_array,cell_size,threshold)
        if return_3d:
            return mask_to_image3d(mask)
        else:
            return mask


    def set_sprite_image(self,img):
        """Set sprites image from a numpy array
        Useful when raw image is transformed using thresholds
        """

        surface = pygame.surfarray.make_surface(img.swapaxes(0,1))
        self.image = surface


    def show(self):
        """Show the current layer in the notebook using matplotlib
        """
        plt.imshow(self.get_img())
        plt.xticks([])
        plt.yticks([])
        plt.show()



    def explore_snap_to_grid(self,save = True):
        """Explore mask transformation snapped to a grid using ipywidgets
        Can be used in the notebook
        Save argument will actually transforms inplace the layer to be used, 
        But we recommend to save and later use .save_img to save a finalized png version of the layer

        Args:
            save (bool, optional): Save cell_size, image, and threshold to attributess. Defaults to True.
        """


        @interact(
            th = FloatSlider(min = 0,max = 1,value = 0.1,step = 0.1),
            cell_size = IntSlider(min = 10,max = 200,value = 20,step = 10)
        )
        def show(th,cell_size):

            # Prepare figure
            fig, (ax1,ax2) = plt.subplots(1, 2,figsize = (8,6))

            # Snap image mask to grid
            img = self.snap_to_grid(threshold = th,cell_size = cell_size,return_3d = True)

            # Show using matplotlib
            ax1.imshow(self.raw_img)
            ax2.imshow(self.snap_to_grid(threshold = th,cell_size = cell_size,return_3d = True))

            # Add titles and removing ticks
            ax1.set_title("Original image")
            ax2.set_title(f"Snap to grid\n'threshold={th}' & 'cell_size={cell_size}'")
            ax1.set_xticks([])
            ax2.set_xticks([])
            ax1.set_yticks([])
            ax2.set_yticks([])
            plt.show()

            # Save last params
            if save:
                self.mask_threshold = th
                self.saved_cell_size = cell_size
                self.set_sprite_image(img)


    def get_navigation_mesh(self):
        """Get a navigation mesh snapped to the grid
        """
        shape = (self.env.height,self.env.width)
        if self.obstacle:
            mesh = mask_to_mesh(self.mask_array,self.env.cell_size,threshold=self.mask_threshold)
            assert mesh.shape == shape
            return mesh
        else:
            return np.zeros(shape)

