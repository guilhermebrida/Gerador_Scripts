

def validate_checkboxes(selected_checkboxes):
    if "6" in selected_checkboxes and "14" in selected_checkboxes:
        return True
    return False

def validate_mifares(selected_checkboxes):
    if "11" in selected_checkboxes and "12" in selected_checkboxes:
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
    if "Nome do Arquivo" not in values or "Id Arquivo configurador" not in values:
        return True
    return False

def validate_cc_id(values):
    if "Customer Child ID" not in values:
        return True
    return False

def validate_function(hw,selected_checkboxes):
    if ('2' in hw or '4' in hw or '5' in hw or '6' in hw) and ('17' in selected_checkboxes or '12' in selected_checkboxes):
        return True
    if ('2' in hw or '3' in hw or '6' in hw) and '16' in selected_checkboxes:
        return True
    return False

    