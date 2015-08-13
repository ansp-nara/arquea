function referente(sel, field)
{
select_ctrl = document.getElementById(sel);
field_ctrl = document.getElementById(field);

txt = select_ctrl.options[select_ctrl.selectedIndex].text
field_ctrl.value = txt;
}
