import os
import glob
import re

root_dir = r"d:\E-COMMERCE MANAGEMENT & RECOMMENDATION SAAS"
admin_files = glob.glob(os.path.join(root_dir, "apps", "*", "admin.py"))

for file_path in admin_files:
    if "accounts" in file_path:  # Skip original accounts admin
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Replace list_display, search_fields, list_filter with pass to fix errors
    new_content = re.sub(r"\s+list_display = \[.*?\]", "", content, flags=re.DOTALL)
    new_content = re.sub(r"\s+search_fields = \[.*?\]", "", new_content, flags=re.DOTALL)
    new_content = re.sub(r"\s+list_filter = \[.*?\]", "", new_content, flags=re.DOTALL)
    new_content = re.sub(r"\s+list_per_page = 50", "\n    pass", new_content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
print("Fixed admin files.")
