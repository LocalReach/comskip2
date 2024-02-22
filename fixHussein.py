import os
from PIL import Image
import shutil
import xml.etree.ElementTree as ET

def hussein_fix(source_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        output_path = os.path.join(output_directory, filename)

        if filename.endswith('.png'):
            with Image.open(file_path) as img:
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    img = img.convert('RGB')
                new_filename = os.path.splitext(filename)[0] + '.jpeg'
                img.save(os.path.join(output_directory, new_filename), 'JPEG')
                
        elif filename.endswith('.xml'):
            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find the <filename> tag and update it
                filename_tag = root.find('filename')
                if filename_tag is not None and filename_tag.text.endswith('.png'):
                    filename_tag.text = filename_tag.text[:-4] + '.jpeg'
                    # Save the updated XML file in the output directory
                    tree.write(os.path.join(output_directory, filename))
                    print(f"Updated {filename} to have a .jpeg extension in filename tag.")
            except ET.ParseError as e:
                print(f"Error parsing {filename}: {e}")

source_directory = 'data1/train'
output_directory = 'data1-jpg/train-jpg'
hussein_fix(source_directory, output_directory)
source_directory = 'data1/validate'
output_directory = 'data1-jpg/validate-jpg'
hussein_fix(source_directory, output_directory)