# Extract Key Colors Node Library

A Griptape node library for extracting dominant colors from images using Pylette's color extraction algorithms.

## Overview

The ExtractKeyColors node analyzes input images to extract the most prominent colors, creating dynamic color picker parameters for each extracted color. The node supports both KMeans and MedianCut algorithms via Pylette, with colors automatically ordered by their frequency in the image.

## Features

- **Dual Algorithm Support**: Choose between KMeans clustering and MedianCut algorithms for color extraction
- **Automatic Frequency Sorting**: Colors are automatically ordered by their prominence in the image
- **Dynamic Parameters**: Creates color picker UI components for each extracted color
- **Flexible Input Support**: Handles ImageArtifact, ImageUrlArtifact, and dictionary formats
- **Configurable Color Count**: Extract 1-12 colors as needed
- **Built-in Color Diversity**: Pylette ensures extracted colors are distinct and representative
- **Robust Error Handling**: Comprehensive error reporting with detailed messages

## How It Works

1. **Image Conversion**: Converts input image to PIL Image format and ensures RGB color space
2. **Algorithm Selection**: Choose between KMeans clustering or MedianCut algorithms for color extraction
3. **Color Extraction**: Uses the selected Pylette algorithm to identify dominant color regions
4. **Automatic Ordering**: Colors are automatically sorted by frequency (most prominent first)
5. **Color Diversity**: Pylette ensures extracted colors are distinct and representative
6. **Dynamic UI Creation**: Generates color picker parameters for each extracted color

## Parameters

### Input Parameters

- **input_image** (ImageUrlArtifact/ImageArtifact): The source image to analyze
  - Supports all PIL-compatible formats: PNG, JPEG, JPG, WEBP, GIF, BMP, TIFF, TGA, ICO, and more
  - File browser integration for easy image selection

- **num_colors** (Integer): Target number of colors to extract
  - Range: 1-12 colors
  - Default: 3 colors
  - Slider UI for easy selection

- **algorithm** (String): Color extraction algorithm to use
  - Options: "KMeans" (default) or "MedianCut"
  - Dropdown selection for easy switching
  - KMeans: Uses clustering to identify dominant color groups
  - MedianCut: Uses recursive color space division for balanced color selection

### Output Parameters

Dynamic color picker parameters are created for each extracted color:
- **color_1, color_2, etc.**: Hexadecimal color values
- Each parameter includes a color picker UI component
- Colors are ordered by prominence (most dominant first)

## Algorithm Details

The node supports two Pylette algorithms for optimal color extraction:

### KMeans Algorithm (Default)
1. **Clustering Approach**: Uses K-means clustering to group similar colors together
2. **Dominant Groups**: Identifies the most prominent color clusters in the image
3. **Frequency Analysis**: Each color includes its frequency/prominence in the image
4. **Versatile**: Works well for general-purpose color extraction across various image types

### MedianCut Algorithm
1. **Recursive Division**: Recursively divides the color space to identify dominant color regions
2. **Balanced Distribution**: Colors are selected to represent the full spectrum of the image
3. **Perceptual Quality**: Optimized for perceptually distinct and representative colors
4. **Efficient Processing**: Fast algorithm that handles images of various sizes effectively

Both algorithms automatically ensure color diversity and prominence-based ordering.

## Use Cases

- **Design Workflows**: Extract color palettes for design projects
- **Brand Analysis**: Analyze dominant colors in logos and marketing materials
- **Image Processing**: Create color-based filters and effects
- **Data Visualization**: Generate color schemes based on image content
- **Creative Tools**: Build color palette generators and design assistants

## Technical Specifications

- **Algorithms**: KMeans clustering and MedianCut via Pylette library
- **Color Space**: RGB (0-255 per channel)
- **Output Format**: Hexadecimal color codes (#RRGGBB)
- **Sorting**: Automatic frequency-based ordering (most prominent first)
- **Color Diversity**: Automatic distinctiveness enforcement by Pylette
- **Algorithm Selection**: Runtime selection via dropdown parameter

## 📦 Installation

### Prerequisites

- [Griptape Nodes](https://github.com/griptape-ai/griptape-nodes) installed and running

### Install the Library

1. **Download the library files** to your Griptape Nodes libraries directory:
   ```bash
   # Navigate to your Griptape Nodes libraries directory
   cd `gtn config show workspace_directory`
   
   # Clone or download this library
   git clone https://github.com/your-username/griptape-nodes-library-keycolors.git
   ```

2. **Add the library** in the Griptape Nodes Editor:
   * Open the Settings menu and navigate to the *Libraries* settings
   * Click on *+ Add Library* at the bottom of the settings panel
   * Enter the path to the library JSON file: **your Griptape Nodes Workspace directory**`/griptape-nodes-library-keycolors/keycolors/griptape_nodes_library.json`
   * You can check your workspace directory with `gtn config show workspace_directory`
   * Close the Settings Panel
   * Click on *Refresh Libraries*

3. **Verify installation** by checking that the ExtractKeyColors node appears in your Griptape Nodes interface under the "Image/KeyColors" category.

### Dependencies

This library automatically installs the following dependencies:
- `Pylette`: For KMeans and MedianCut-based color palette extraction
- `Pillow`: For image processing and format conversion
- `griptape-nodes`: Core Griptape nodes framework

## Example Output

```
Color 1: RGB(214, 206, 201) | Hex: #d6cec9  (Most prominent)
Color 2: RGB( 51,  15,  15) | Hex: #330f0f  (Second most prominent)  
Color 3: RGB(213,   9,  18) | Hex: #d50912  (Third most prominent)
```

## Debug Information

When debug logging is enabled, the node provides detailed information about:
- Selected algorithm (KMeans or MedianCut) and extraction results
- Frequency/prominence data for each color
- RGB values and hexadecimal color codes
- Image processing and conversion steps

## Error Handling

The node includes comprehensive error handling for:
- Invalid or corrupted image data
- Unsupported image formats
- Network issues with ImageUrlArtifact
- Pylette processing failures
- Image conversion and color space issues

## Performance Considerations

- Both KMeans and MedianCut algorithms are optimized for speed and accuracy
- KMeans clustering efficiently handles complex color distributions
- MedianCut's recursive division handles images of various sizes effectively
- Automatic color space conversion ensures compatibility
- Clean, maintainable implementation with minimal complexity

---

This node provides a professional-grade solution for color extraction using modern, actively-maintained libraries, making it ideal for both creative and technical workflows.
