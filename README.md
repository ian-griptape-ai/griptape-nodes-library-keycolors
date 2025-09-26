# Extract Key Colors Node Library

A Griptape node library for extracting dominant colors from images using advanced color analysis and prominence-based ordering.

## Overview

The ExtractKeyColors node analyzes input images to extract the most prominent colors, creating dynamic color picker parameters for each extracted color. The node combines ColorThief's sophisticated color analysis with pixel frequency analysis to ensure colors are ordered by their actual dominance in the image.

## Features

- **Hybrid Color Extraction**: Combines ColorThief's advanced color analysis with prominence-based ordering
- **True Dominance Ordering**: Colors are ordered by actual pixel frequency in the image
- **Dynamic Parameters**: Creates color picker UI components for each extracted color
- **Flexible Input Support**: Handles ImageArtifact, ImageUrlArtifact, and dictionary formats
- **Configurable Color Count**: Extract 1-12 colors as needed
- **Automatic Deduplication**: Filters out similar colors to ensure diversity
- **Robust Error Handling**: Graceful fallbacks and comprehensive error reporting

## How It Works

1. **ColorThief Extraction**: Uses ColorThief to extract a sophisticated color palette
2. **Prominence Analysis**: Analyzes pixel distribution to determine actual color dominance
3. **Intelligent Ordering**: Orders ColorThief colors by their true prominence in the image
4. **Diversity Filtering**: Ensures selected colors are sufficiently different from each other
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

The node uses a hybrid approach that combines the best of both worlds:

1. **ColorThief Analysis**: Leverages ColorThief's sophisticated color clustering and perceptual analysis
2. **Pixel Frequency Counting**: Analyzes actual pixel distribution to determine true prominence
3. **Distance-Based Matching**: Uses Euclidean distance in RGB space to match pixels to ColorThief colors
4. **Diversity Enforcement**: Ensures minimum color distance (30 RGB units) between selected colors
5. **Performance Optimization**: Resizes large images to 400px for faster processing while maintaining accuracy

## Use Cases

- **Design Workflows**: Extract color palettes for design projects
- **Brand Analysis**: Analyze dominant colors in logos and marketing materials
- **Image Processing**: Create color-based filters and effects
- **Data Visualization**: Generate color schemes based on image content
- **Creative Tools**: Build color palette generators and design assistants

## Technical Specifications

- **Color Space**: RGB (0-255 per channel)
- **Output Format**: Hexadecimal color codes (#RRGGBB)
- **Processing Size**: Images resized to max 400px for analysis (maintains aspect ratio)
- **Color Distance**: Minimum 30 RGB units between selected colors
- **Fallback Behavior**: Graceful degradation to standard ColorThief if prominence analysis fails

## Installation

This library requires the following dependencies:
- `colorthief`: For sophisticated color palette extraction
- `Pillow`: For image processing and analysis
- `griptape-nodes`: Core Griptape nodes framework

## Example Output

```
Color 1: RGB(214, 206, 201) | Hex: #d6cec9  (Most prominent)
Color 2: RGB( 51,  15,  15) | Hex: #330f0f  (Second most prominent)  
Color 3: RGB(213,   9,  18) | Hex: #d50912  (Third most prominent)
```

## Debug Information

When debug logging is enabled, the node provides detailed information about:
- ColorThief palette extraction results
- Pixel frequency analysis for each color
- Color selection and filtering decisions
- Performance metrics and processing steps

## Error Handling

The node includes comprehensive error handling for:
- Invalid or corrupted image data
- Unsupported image formats
- Network issues with ImageUrlArtifact
- ColorThief processing failures
- Memory constraints with large images

## Performance Considerations

- Images are automatically resized for optimal processing speed
- Color analysis is optimized for accuracy vs. performance balance
- Memory usage is managed through efficient pixel processing
- Fallback mechanisms ensure reliable operation

---

This node provides a professional-grade solution for color extraction that combines sophisticated analysis with practical usability, making it ideal for both creative and technical workflows.
