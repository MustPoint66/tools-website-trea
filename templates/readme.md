# Template Hub

This directory contains PDF templates for various document types. The templates are organized by category:

- `resume/`: Resume templates
- `cv/`: CV templates
- `cover_letter/`: Cover letter templates
- `invoice/`: Invoice templates
- `contract/`: Contract templates
- `business/`: Business document templates
- `personal/`: Personal document templates
- `legal/`: Legal document templates
- `academic/`: Academic document templates
- `other/`: Other templates

## Template Structure

Each template has the following components:

1. A PDF file with form fields that can be filled
2. A preview image (PNG) showing how the template looks
3. Metadata in the `metadata.json` file at the root of this directory

## Adding New Templates

To add a new template:

1. Place the PDF file in the appropriate category directory
2. Create a preview image of the template
3. Update the metadata.json file with the template information

Alternatively, use the Template Hub API to upload and manage templates.

## Template Metadata

The metadata.json file contains information about all templates, including:

- Template ID
- Name
- Description
- Category
- Tags
- Preview image path
- File path

## Using Templates

Templates can be filled using the Template Hub API. The API provides endpoints for:

- Listing available templates
- Getting template details
- Filling templates with data
- Downloading filled templates