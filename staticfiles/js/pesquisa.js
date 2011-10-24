function muda_l3(x){
  nt = document.getElementById('id_l3_0')
  if (x == nt) {
    if(x.checked){
        for(i=1;i<5;i++){
           document.getElementById('id_l3_'+i).checked=false;
        }
     }
     else {
        var l = false;
        for(i=1;i<5;i++){
           if(document.getElementById('id_l3_'+i).checked) {
             l = true;
           }
        }
        if (l == false){
            x.checked=true;
        }
     }
  }
  else {
    if(x.checked){
        document.getElementById('id_l3_0').checked=false;
    }else{
        var l = true;
        for(i=1;i<5;i++){
            if(document.getElementById('id_l3_'+i).checked){
                l = false;
            }
        }
        if(l){
            document.getElementById('id_l3_0').checked=true;
        }
    }
  }
}