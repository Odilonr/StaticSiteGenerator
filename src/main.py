from textnode import markdown_to_html_node
import os
import shutil
import re


def main():
   copy_directory_content('static','public')
   generate_pages_recursive('content', 'template.html', 'public')


def delete_folder_content(file_path):
   for entry in os.listdir(file_path):
      path = os.path.join(file_path,entry)
      if os.path.isfile(path) or os.path.islink(path):
         os.unlink(path)
      else:
         shutil.rmtree(path)

def copy_directory_content(source, destination):
   cwd = os.getcwd()
   source_path = os.path.join(cwd, source)
   destination_path = os.path.join(cwd, destination)
   print(destination_path)
   delete_folder_content(destination_path)
   entries = os.listdir(source_path)
   for entry in entries:
      if os.path.isfile(os.path.join(source_path,entry)):
         shutil.copy(os.path.join(source_path,entry), destination_path)
         print(f"{entry} added")
      else:
         os.mkdir(os.path.join(destination_path,entry))
         copy_directory_content(os.path.join(source, entry), os.path.join(destination, entry))

def extract_title(markdown):
   header_match = re.match(r"(#)\s(?!\s)(.+)", markdown)

   if not header_match:
      raise Exception('No Header')
   return header_match.group(0)[2:]

def generate_page(from_path, template_path, dest_path):
   print(f"Generating Page from {from_path} to {dest_path} using {template_path}")
   f = open(from_path, encoding='utf-8')
   markdown_file = f.read()
   f.close()
   f = open(template_path, encoding="utf-8")
   template_file = f.read()
   f.close()
   html_from_markdown = markdown_to_html_node(markdown_file).to_html()
   page_title = extract_title(markdown_file)
   template_file = template_file.replace('{{ Title }}',page_title)
   template_file = template_file.replace('{{ Content }}', html_from_markdown)
   dest_directory = os.path.dirname(dest_path)
   os.makedirs(dest_directory, exist_ok=True)
   f = open(dest_path, 'w', encoding="utf-8")
   f.write(template_file)
   f.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
   entries = os.listdir(dir_path_content)
   for entry in entries:
      if os.path.isfile(os.path.join(dir_path_content,entry)):
         from_path = os.path.join(dir_path_content,entry)
         dest_path = os.path.join(dest_dir_path, entry.replace('.md','.html'))
         generate_page(from_path, template_path, dest_path)
      else:
         os.mkdir(os.path.join(dest_dir_path, entry))
         generate_pages_recursive(os.path.join(dir_path_content,entry), template_path, os.path.join(dest_dir_path, entry))
         










  




main()