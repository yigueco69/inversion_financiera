function Verificador(){
	codigoDeBarras = ''
    tiempo = 10000
    temp = null
    $(document).keypress(evento);


    function cambiar(argument) {
        // body...
    }
    function evento(evento){
    	if(evento.which == 13){
    		console.log("entro")
    		function explode(){
                $('#intro').show()
                temp = null;
            }
            if(temp!=null){
                clearTimeout(temp);
            }
            temp = setTimeout(explode, tiempo);
    		codigoDeBarrasEan13=codigoDeBarras.substring(0,13)
    		codigoDeBarrasPeso=codigoDeBarras.substring(13,17)
    		console.log(codigoDeBarrasPeso)
    		codigoDeBarras = ""
    		new openerp.web.Model('product.product').query(['display_name','list_price','product_tmpl_id','image_medium']).filter([['ean13','like',codigoDeBarrasEan13],['sale_ok','=',true],['available_in_pos','=',true]]).context(null).all()
                .then(function(result){
                    nombre = result[0].display_name;
                    precio = result[0].list_price;
                    image_medium = result[0].image_medium


                    new openerp.web.Model('ir.translation').query(['value']).filter([['name','=','product.template,name'],['res_id','=',result[0].product_tmpl_id[0]]]).context(null).all()
                        .then(function(trad){
                            if(trad[0] != undefined){
                                nombre = trad[0].value    
                            }
                        });
                    $('#nombre').html(nombre)
                    $('#precio').html(precio)
                    img = new Image();
                    if(image_medium){
                        console.log(image_medium);
                        img.src = "data:image/png;base64,"+image_medium
                    }else{
                        img.src = "/verificador_precios/static/src/img/imgNoDisponible.png"
                    }
                    
                    
                    $('#imagen').html(img)
                    // $('#fecha').html(result[0].fecha_inscripcion)
                    new openerp.web.Model('product.presentacion').query(['descripcion','name','precio']).filter([['product_id','=',result[0].product_tmpl_id[0]]]).context(null).all()
                    .then(function(result){    
                        $('#variantes').empty();
                        for (var i = 0; i < result.length; i++) {
                            var span = document.createElement('span')
                            console.log((parseFloat(codigoDeBarrasPeso)/100)+"-"+parseFloat(result[i].name));
                            if((parseFloat(codigoDeBarrasPeso)/100) == parseFloat(result[i].name)){
                                console.log("es este"+result[i].name);
                                $('#variantes').append( "<span style='color:red'>"+result[i].descripcion+' - '+result[i].name+' - '+result[i].precio+"</span></br>" );
                            }else{
                                $('#variantes').append( "<span>"+result[i].descripcion+' - '+result[i].name+' - '+result[i].precio+"</span></br>" );
                            }
                        } 
                        console.log(result)
                    })
                    $('#intro').hide()

                        
                	console.log(result)
                    
                })


    	}else{
    		codigoDeBarras+=evento.key
    	}
    	//console.log(codigoDeBarras)
           
    	
    }

}


    
