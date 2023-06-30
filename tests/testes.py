
def deve_receber_um_customer_child_id_e_retornar_como_uma_tag():
    child_id = 123456
    assert customer_child_id(child_id) == '[cc.id] 123456 [cc.id]'
