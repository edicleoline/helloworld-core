from __future__ import annotations

import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('scripts/templates'))

def create_use_case(target_path: str, feature_name: str):
    use_case_path = os.path.join(target_path, "use_cases")
    os.makedirs(use_case_path, exist_ok=True)

    use_case_filename = "create"

    template = env.get_template('use_case.j2')
    rendered_class = template.render()
    file_name = os.path.join(use_case_path, f"{use_case_filename.lower()}.py")

    with open(file_name, 'w') as f:
        f.write(rendered_class)


def create_feature():
    # output_path = input("Where is the target (e.g.,: /home/edicleo/dev/helloworld/backend/libs/media/helloworld/media/features)? ").strip()
    output_path = "/home/edicleo/dev/helloworld/backend/libs/media/helloworld/media/features".strip()

    feature_name = input("What will be the name of the feature? (e.g., user_comment)? ").strip() or "user_comment" #todo: remove!

    create_repository = input("Do you need a Repository? (y/n) [y]: ").lower() or "y"

    if create_repository == "y":
        repository_adapter = input("What adapter will you use for the Repository? (sqlalchemy/motor) [sqlalchemy]: ").lower() or "sqlalchemy"

    started = input("Let's start now. Can I continue? (y/n) [y]: ").lower() or "y"

    output_path = os.path.join(output_path, f"{feature_name.lower()}")

    os.makedirs(output_path, exist_ok=True)

    create_use_case(output_path, feature_name)



def _create_feature():
    pass

if __name__ == "__main__":
    create_feature()