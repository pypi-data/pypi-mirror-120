def lw_login_reverse(obj, mode=''):
    if mode == 'hide':
        obj.btn_lw_login_record.setIcon(icon('fa.angle-down', color='silver'))
        obj.lw_login_record.reverse_state()
        obj.lw_login_record.hide()
    elif mode == 'show':
        obj.btn_lw_login_record.setIcon(icon('fa.angle-up', color='silver'))
        obj.lw_login_record.reverse_state()
        obj.lw_login_record.show()