# Extract Key Colors Node Library

A Griptape node library for extracting dominant colors from images using Pylette's KMeans clustering algorithm.

## Overview

The ExtractKeyColors node analyzes input images to extract the most prominent colors, creating dynamic color picker parameters for each extracted color. The node uses Pylette's KMeans clustering algorithm which automatically orders colors by their frequency in the image.

## Features

- **KMeans Clustering**: Uses Pylette's optimized KMeans algorithm for perceptual color extraction
- **Automatic Frequency Sorting**: Colors are automatically ordered by their prominence in the image
- **Dynamic Parameters**: Creates color picker UI components for each extracted color
- **Flexible Input Support**: Handles ImageArtifact, ImageUrlArtifact, and dictionary formats
- **Configurable Color Count**: Extract 1-12 colors as needed
- **Built-in Color Diversity**: Pylette ensures extracted colors are distinct and representative
- **Robust Error Handling**: Comprehensive error reporting with detailed messages

## How It Works

1. **Image Conversion**: Converts input image to PIL Image format and ensures RGB color space
2. **KMeans Clustering**: Uses Pylette's KMeans algorithm to identify dominant color clusters
3. **Automatic Ordering**: Colors are automatically sorted by frequency (most prominent first)
4. **Color Diversity**: Pylette ensures extracted colors are distinct and representative
5. **Dynamic UI Creation**: Generates color picker parameters for each extracted color

## Parameters

### Input Parameters

- **input_image** (ImageUrlArtifact/ImageArtifact): The source image to analyze
  - Supports common formats: JPG, PNG, GIF, BMP, TIFF, ICO, WEBP
  - File browser integration for easy image selection

- **num_colors** (Integer): Target number of colors to extract
  - Range: 1-12 colors
  - Default: 3 colors
  - Slider UI for easy selection

### Output Parameters

Dynamic color picker parameters are created for each extracted color:
- **color_1, color_2, etc.**: Hexadecimal color values
- Each parameter includes a color picker UI component
- Colors are ordered by prominence (most dominant first)

## Algorithm Details

The node uses Pylette's KMeans clustering algorithm for optimal color extraction:

1. **KMeans Clustering**: Groups similar pixels into clusters to identify dominant colors
2. **Perceptual Grouping**: Colors are selected based on perceptual similarity and distribution
3. **Frequency Analysis**: Each color includes its frequency/prominence in the image
4. **Automatic Diversity**: Pylette ensures selected colors are distinct and representative
5. **Optimized Processing**: Efficient algorithm handles images of various sizes effectively

## Use Cases

- **Design Workflows**: Extract color palettes for design projects
- **Brand Analysis**: Analyze dominant colors in logos and marketing materials
- **Image Processing**: Create color-based filters and effects
- **Data Visualization**: Generate color schemes based on image content
- **Creative Tools**: Build color palette generators and design assistants

## Technical Specifications

- **Algorithm**: KMeans clustering via Pylette library
- **Color Space**: RGB (0-255 per channel)
- **Output Format**: Hexadecimal color codes (#RRGGBB)
- **Sorting**: Automatic frequency-based ordering (most prominent first)
- **Color Diversity**: Automatic distinctiveness enforcement by Pylette

## Installation

This library requires the following dependencies:
- `Pylette`: For KMeans-based color palette extraction
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
- Pylette KMeans extraction results
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

- Pylette's KMeans algorithm is optimized for speed and accuracy
- Efficient clustering handles images of various sizes
- Automatic color space conversion ensures compatibility
- Clean, maintainable implementation with minimal complexity

---

This node provides a professional-grade solution for color extraction using modern, actively-maintained libraries, making it ideal for both creative and technical workflows.
