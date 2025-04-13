import shutil
import os
from markdown_blocks import *

def copy_dir2dir(source, destination):
    #raise exception if source doesn't exist. delete destination if it exists
    if not os.path.exists(source):
        raise Exception("Source directory does not exist")
    if os.path.exists(destination):
        shutil.rmtree(destination)

    #create destination folder
    os.mkdir(destination)

    def copy_recursively(current_src, current_dst):
        for item in os.listdir(current_src):

            #ignore dot-prefixed items
            if not item.startswith('.'):
                item_path = os.path.join(current_src, item)
                #base case: file
                if os.path.isfile(item_path):
                    shutil.copy(item_path, current_dst)

                    print(f"Copying file: {item_path} --> {current_dst}")
                elif os.path.isdir(item_path):
                    new_path = os.path.join(current_dst, item)
                    os.mkdir(new_path)
                    print(f"Created directory: {new_path}, descending...")

                    copy_recursively(item_path, new_path)
    
    copy_recursively(source, destination)

def extract_title(markdown):
    lines = markdown.split('\n')
    titles = []
    for line in lines:
        if line.startswith("#") and not line.startswith("##"):
            titles.append(line)
    num = len(titles)
    if num != 1:
        raise Exception(f"Expected 1 title element, found {num}.")
    else:
        return titles[0].strip("#").strip()
    
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as from_file, \
        open(template_path, "r") as template_file, \
        open(dest_path, "w") as dest_file:

        # Read from the existing files
        from_content = from_file.read()
        template_content = template_file.read()

        # Process the content
        html = markdown_to_html_node(from_content).to_html()
        title = extract_title(from_content)

        # Replace placeholders
        final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

        # Write to the destination file
        dest_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, item)
        
        if os.path.isfile(full_path):
            file_name, file_extension = os.path.splitext(full_path)
            if file_extension == ".md":
                relative_path = os.path.relpath(full_path, dir_path_content)
                destination_path = os.path.join(dest_dir_path, os.path.splitext(relative_path)[0] + ".html")
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)
                generate_page(full_path, template_path, destination_path)
        elif os.path.isdir(full_path):
            # Adjust dest_dir_path for subdirectory
            new_dest_dir_path = os.path.join(dest_dir_path, os.path.relpath(full_path, dir_path_content))
            generate_pages_recursive(full_path, template_path, new_dest_dir_path)

            

def main():
    copy_dir2dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")
main()
