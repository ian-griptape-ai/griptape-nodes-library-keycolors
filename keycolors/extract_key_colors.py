import logging
import base64
import uuid
import io
import hashlib
from collections import Counter
from PIL import Image 

from griptape_nodes.exe_types.core_types import Parameter, ParameterMode
from griptape_nodes.exe_types.node_types import DataNode
from griptape_nodes.exe_types.core_types import ParameterTypeBuiltin
from griptape_nodes.traits.slider import Slider
from griptape_nodes.traits.color_picker import ColorPicker

from griptape.artifacts import ImageArtifact, ImageUrlArtifact

from colorthief import ColorThief

logger = logging.getLogger(__name__)

__all__ = ["ExtractKeyColors"]

class ExtractKeyColors(DataNode):
    """A node that extracts dominant colors from images using the ColorThief algorithm.
    
    This node analyzes an input image and extracts the most prominent colors,
    creating dynamic color picker parameters for each extracted color. The colors
    are provided in both RGB and hexadecimal formats for easy use in design workflows.
    
    Features:
    - Supports ImageArtifact and ImageUrlArtifact inputs
    - Configurable number of colors to extract (3-12)
    - Dynamic color picker parameters for each extracted color
    - Pretty-printed color output for inspection
    - Automatic parameter cleanup between runs
    """
    
    def __init__(self, **kwargs) -> None:
        """Initialize the ExtractKeyColors node with input parameters.
        
        Sets up the node with:
        - input_image: Parameter for the source image
        - num_colors: Parameter for the target number of colors to extract
        - number_of_color_params: Internal counter for dynamic parameters
        
        Args:
            **kwargs: Additional keyword arguments passed to the parent DataNode
        """
        super().__init__(**kwargs)

        self.number_of_color_params = 0 # Internal counter for dynamic parameters

        self.add_parameter(
            Parameter(
            name="input_image",
            tooltip="The image to extract key colors from",
            type="ImageUrlArtifact",
            allowed_modes=[ParameterMode.INPUT,ParameterMode.PROPERTY],
            input_types=["ImageUrlArtifact","ImageArtifact"],
            ui_options={
                "display_name":"Input Image",
                "clickable_file_browser":True,
                "file_browser_options":{
                    "extensions":["jpg","jpeg","png","gif","bmp","tiff","ico","webp"],
                    "allow_multiple":False,
                    "allow_directories":False
                }
            }
            )
        )

        self.add_parameter(
            Parameter(
                name="num_colors",
                tooltip="Target number of colors to extract",
                type=ParameterTypeBuiltin.INT.value,
                traits={Slider(min_val=1,max_val=12)},
                default_value=3,
                allowed_modes=[ParameterMode.INPUT,ParameterMode.PROPERTY],
                ui_options={"display_name":"Target Number of Colors"},
            )
        )
   
    def _dict_to_image_url_artifact(self, image_dict: dict, image_format: str | None = None) -> ImageUrlArtifact:
        """Convert a dictionary representation of an image to an ImageUrlArtifact.
        
        This method handles serialized image artifacts that come as dictionaries,
        typically when artifacts are passed between nodes in the workflow system.
        It supports both direct URL references and base64-encoded image data.
        
        Args:
            image_dict: Dictionary containing image data with 'value' and 'type' keys
            image_format: Optional format override (e.g., 'png', 'jpg'). If None,
                         format is inferred from MIME type or defaults to 'png'
        
        Returns:
            ImageUrlArtifact: A URL-based image artifact that can be processed
            
        Raises:
            KeyError: If required dictionary keys are missing
            ValueError: If base64 decoding fails or image data is invalid
        """
        from griptape_nodes.retained_mode.griptape_nodes import GriptapeNodes
        
        value = image_dict["value"]
        if image_dict.get("type") == "ImageUrlArtifact":
            return ImageUrlArtifact(value)

        # Strip base64 prefix if needed
        if "base64," in value:
            value = value.split("base64,")[1]

        image_bytes = base64.b64decode(value)

        # Infer format from MIME type if not specified
        if image_format is None:
            if "type" in image_dict:
                mime_format = image_dict["type"].split("/")[1] if "/" in image_dict["type"] else None
                image_format = mime_format
            else:
                image_format = "png"

        url = GriptapeNodes.StaticFilesManager().save_static_file(image_bytes, f"{uuid.uuid4()}.{image_format}")
        return ImageUrlArtifact(url)

    def _image_to_bytes(self, image_artifact) -> bytes:
        """Convert ImageArtifact, ImageUrlArtifact, or dict representation to bytes.
        
        Args:
            image_artifact: ImageArtifact, ImageUrlArtifact, or dict representation
            
        Returns:
            Image data as bytes
            
        Raises:
            ValueError: If image artifact is invalid or unsupported
        """
        if not image_artifact:
            raise ValueError("No input image provided")
        
        try:
            # Handle dictionary format (serialized artifacts)
            if isinstance(image_artifact, dict):
                # Convert dict to ImageUrlArtifact first
                image_url_artifact = self._dict_to_image_url_artifact(image_artifact)
                image_bytes = image_url_artifact.to_bytes()
            # Handle artifact objects directly
            elif isinstance(image_artifact, (ImageArtifact, ImageUrlArtifact)):
                image_bytes = image_artifact.to_bytes()
            else:
                # Try to convert to bytes if it's a different artifact type
                image_bytes = image_artifact.to_bytes()
            
            # Verify we have image data
            if not image_bytes or len(image_bytes) < 100:
                raise ValueError("Image data is empty or too small")
            
            return image_bytes
            
        except Exception as e:
            raise ValueError(f"Failed to extract image data: {str(e)}")

    def _get_colors_by_prominence(self, image_bytes: bytes, num_colors: int) -> list[tuple[int, int, int]]:
        """Extract colors using ColorThief and order them by actual prominence in the image.
        
        This method first uses ColorThief to extract a palette of colors using its
        sophisticated color analysis, then analyzes the actual pixel distribution
        to order those colors by their true prominence in the image.
        
        Args:
            image_bytes: Raw image data as bytes
            num_colors: Number of colors to extract
            
        Returns:
            List of RGB tuples ordered by prominence (most prominent first)
            
        Raises:
            ValueError: If image processing fails
        """
        try:
            # First, use ColorThief to extract a larger palette for analysis
            image_io = io.BytesIO(image_bytes)
            color_thief = ColorThief(image_io)
            # Extract more colors than needed to have options for prominence ordering
            palette_size = max(15, num_colors * 2)
            colorthief_palette = color_thief.get_palette(color_count=palette_size)
            
            logger.debug(f"ColorThief extracted {len(colorthief_palette)} colors for prominence analysis")
            
            # Now analyze the image to count pixel frequencies for each ColorThief color
            image = Image.open(io.BytesIO(image_bytes))
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image for faster processing while maintaining color accuracy
            max_size = 400
            if image.width > max_size or image.height > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Get all pixels for analysis
            pixels = list(image.getdata())
            
            # Calculate prominence score for each ColorThief color
            color_scores = []
            min_distance = 30  # Distance threshold for color matching
            
            for ct_color in colorthief_palette:
                r, g, b = ct_color
                
                # Count pixels that are close to this ColorThief color
                pixel_count = 0
                for pixel in pixels:
                    pr, pg, pb = pixel
                    # Calculate distance between pixel and ColorThief color
                    distance = ((r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2) ** 0.5
                    if distance <= min_distance:
                        pixel_count += 1
                
                color_scores.append((ct_color, pixel_count))
                logger.debug(f"ColorThief color RGB({r:3d}, {g:3d}, {b:3d}) matches {pixel_count} pixels")
            
            # Sort by pixel count (prominence) in descending order
            color_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Extract the top colors and ensure diversity
            selected_colors = []
            for color, count in color_scores:
                if len(selected_colors) >= num_colors:
                    break
                    
                r, g, b = color
                
                # Check if this color is too similar to already selected colors
                is_similar = False
                for existing_color in selected_colors:
                    er, eg, eb = existing_color
                    distance = ((r - er) ** 2 + (g - eg) ** 2 + (b - eb) ** 2) ** 0.5
                    if distance < min_distance:
                        is_similar = True
                        break
                
                if not is_similar:
                    selected_colors.append(color)
                    logger.debug(f"Selected prominent ColorThief color: RGB({r:3d}, {g:3d}, {b:3d}) - {count} pixels")
            
            return selected_colors[:num_colors]
            
        except Exception as e:
            logger.warning(f"Prominence-based ColorThief ordering failed: {e}, using default ColorThief palette")
            # Fallback to standard ColorThief if our analysis fails
            image_io = io.BytesIO(image_bytes)
            color_thief = ColorThief(image_io)
            return color_thief.get_palette(color_count=num_colors)

    def _clear_color_picker_parameters(self) -> None:
        """Clear all dynamically created color picker parameters.
        
        This method removes all previously created color parameters (color_1, color_2, etc.)
        to prevent duplicate parameter errors when the node runs again with different
        numbers of colors. It also resets the internal parameter counter.
        
        The method safely checks for parameter existence before attempting removal
        to avoid errors if parameters don't exist.
        """
        # Clear all color parameters that might exist (up to 15 since we extract max 15)
        for i in range(1, 16):  # Clear up to color_15 to be safe
            param_name = f"color_{i}"
            if self.get_parameter_by_name(param_name) is not None:
                logger.debug(f"Removing existing parameter: {param_name}")
                # Clear parameter values first
                if param_name in self.parameter_values:
                    del self.parameter_values[param_name]
                if param_name in self.parameter_output_values:
                    del self.parameter_output_values[param_name]
                # Remove the parameter itself
                self.remove_parameter_element_by_name(param_name)
        
        self.number_of_color_params = 0

    def process(self) -> None:
        """Main processing method that extracts colors from the input image.
        
        This method performs the following steps:
        1. Clears any existing color parameters from previous runs
        2. Retrieves the input image and target number of colors
        3. Converts the image artifact to bytes for processing
        4. Uses ColorThief to extract a sophisticated color palette
        5. Analyzes pixel frequency to order ColorThief colors by prominence
        6. Filters out similar colors to ensure diversity
        7. Creates dynamic color picker parameters for each selected color
        8. Logs color information for inspection
        
        The algorithm combines ColorThief's sophisticated color analysis with
        prominence-based ordering. ColorThief extracts high-quality colors, then
        pixel frequency analysis orders them by actual dominance in the image.
        
        The selected colors are made available as dynamic output parameters
        named color_1, color_2, etc., each containing the hexadecimal color value
        and featuring a color picker UI component.
        
        Raises:
            ValueError: If image processing fails or no colors can be extracted
            Exception: If ColorThief processing encounters an error
        """
        self._clear_color_picker_parameters()
        
        # Force parameter refresh to avoid caching issues
        if "input_image" in self.parameter_output_values:
            del self.parameter_output_values["input_image"]
        
        input_image = self.get_parameter_value("input_image")
        num_colors = self.get_parameter_value("num_colors")
        
        # Debug: Log image artifact information to detect caching issues
        if hasattr(input_image, 'value'):
            image_id = str(input_image.value)[:50] + "..." if len(str(input_image.value)) > 50 else str(input_image.value)
            logger.debug(f"Processing image: {image_id}")
        elif isinstance(input_image, dict):
            image_id = str(input_image.get('value', 'unknown'))[:50] + "..." if len(str(input_image.get('value', 'unknown'))) > 50 else str(input_image.get('value', 'unknown'))
            logger.debug(f"Processing image dict: {image_id}")
        else:
            logger.debug(f"Processing image of type: {type(input_image)}")
            
        logger.debug(f"Extracting {num_colors} colors from input image")
        image_bytes = self._image_to_bytes(input_image)
        
        # Debug: Create hash to detect if the same image data is being processed
        image_hash = hashlib.md5(image_bytes).hexdigest()[:8]
        logger.debug(f"Image data hash: {image_hash} (size: {len(image_bytes)} bytes)")
        
        # Extract colors ordered by actual prominence in the image
        selected_colors = self._get_colors_by_prominence(image_bytes, num_colors)
        selected_count = len(selected_colors)
        
        logger.debug(f"Extracted {selected_count} colors ordered by prominence")
        self.number_of_color_params = selected_count

        for i, color in enumerate(selected_colors, 1):
            r, g, b = color
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            logger.debug(f"  Color {i}: RGB({r:3d}, {g:3d}, {b:3d}) | Hex: {hex_color}")
            
            param_name = f"color_{i}"
            logger.debug(f"Creating parameter {param_name} with value {hex_color}")
            
            self.add_parameter(
                Parameter(
                name=param_name,
                default_value=hex_color,
                allowed_modes=[ParameterMode.PROPERTY,ParameterMode.OUTPUT],
                type="str",
                tooltip="Hex color",
                traits={ColorPicker(format="hex")},
                )
            )      

        return