# backend/fastapi_backend/webenv/services/github_service.py
def parse_github_tree(data: dict):
    """
    Github API returns a tree structure of the repository.
    """
    if "tree" not in data:
        return []
    
    tree_structure = []
    for item in data["tree"]:
        path_parts = item["path"].split("/")
        tree_structure.append({
            "type": item["type"],
            "name": path_parts[-1],
            "path": path_parts,
            "depth": len(path_parts)
        })
    return tree_structure
