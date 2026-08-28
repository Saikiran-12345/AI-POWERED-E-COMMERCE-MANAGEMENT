import os

root_dir = r"d:\E-COMMERCE MANAGEMENT & RECOMMENDATION SAAS"
forms_path = os.path.join(root_dir, "apps", "accounts", "forms.py")

with open(forms_path, "r", encoding="utf-8") as f:
    content = f.read()

new_content = content.replace(
    "class UserLoginForm(forms.Form):\n",
    "class UserLoginForm(forms.Form):\n    def __init__(self, request=None, *args, **kwargs):\n        self.request = request\n        super().__init__(*args, **kwargs)\n\n"
)

with open(forms_path, "w", encoding="utf-8") as f:
    f.write(new_content)
