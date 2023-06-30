

def validate_checkboxes(selected_checkboxes):
    if "7" in selected_checkboxes and "15" in selected_checkboxes:
        return True
    return False

def validate_hardwares(selected_hardwares):
    if len(selected_hardwares) > 1:
        return True
    return False

def hardwares_is_None(selected_hardwares):
    if len(selected_hardwares) == 0:
        return True
    return False

def validate_path(values):
    print(values)
    if "Nome do Arquivo" not in values or "Id Arquivo configurador" not in values:
        return True
    return False