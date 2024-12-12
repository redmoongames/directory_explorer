from typing import Dict, Union, List


class GeneratorProjectStructure:
    """
    Generates a human-readable tree structure from a filtered list of directories and files.
    """

    def generate(self, structure: Dict[str, Union[List[str], Dict]]) -> str:
        """
        Generate a human-readable string representation of the project structure.

        Args:
            structure (Dict[str, Union[List[str], Dict]]): Filtered structure containing directories and files.

        Returns:
            str: A formatted string representing the project structure.
        """
        result = []

        def recurse(path: str, content: Dict[str, List[str]], indent: int = 0):
            result.append(f"{' ' * indent}{path}/")
            for directory in content.get("directories", []):
                result.append(f"{' ' * (indent + 2)}{directory}/")
            for file in content.get("files", []):
                result.append(f"{' ' * (indent + 2)}{file}")

        for root, content in structure.items():
            recurse(root, content)

        return "\n".join(result)